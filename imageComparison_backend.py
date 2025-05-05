import os
import datetime
import pickle
import numpy as np
import time
from deepface import DeepFace
from retinaface import RetinaFace
import tensorflow as tf
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

THRESHOLD = 0.7
MODEL_NAME = "ArcFace"
DETECTOR_BACKEND = "retinaface"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_DIR = "/content/drive/MyDrive/Colab Notebooks/test"

# Initialize timing dictionary
timings = {}

def start_timing(phase):
    timings[phase] = time.time()

def end_timing(phase):
    if phase in timings:
        elapsed = time.time() - timings[phase]
        print(f"{phase} took: {elapsed:.2f} seconds")
        return elapsed
    return 0

# GPU memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    print(f"Using GPU(s): {[gpu.name for gpu in gpus]}")
else:
    print("No GPU detected. Running on CPU.")

def cosine_distance(vector1, vector2):
    """Calculate cosine distance between two vectors"""
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    return 1 - (dot_product / (norm1 * norm2))

@lru_cache(maxsize=100)
def detect_face_once(image_path):
    """Cached face detection function"""
    try:
        start_timing("face_detection")
        detections = RetinaFace.detect_faces(image_path)
        end_timing("face_detection")
        return bool(detections)
    except Exception:
        end_timing("face_detection")
        return False

def verify_pair(args):
    img_path, matched_path = args
    try:
        if not detect_face_once(matched_path):
            return None
        
        start_timing("pair_verification")
        result = DeepFace.verify(
            img1_path=img_path,
            img2_path=matched_path,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            align=True
        )
        end_timing("pair_verification")
        
        distance = result.get("distance", 1.0)
        if distance <= THRESHOLD:
            return {
                "match_found": True,
                "matched_image": matched_path,
                "distance": distance,
                "verified": result.get("verified"),
                "raw_result": result
            }
    except Exception as e:
        end_timing("pair_verification")
        print(f"Error verifying {matched_path}: {e}")
    return None

def create_representations_db(db_path):
    """Pre-compute and save face representations for all images in the database"""
    representations = []
    total_images = 0
    processed_images = 0
    
    for root, _, files in os.walk(db_path):
        total_images += len([f for f in files if f.lower().endswith(('png', 'jpg', 'jpeg'))])
    
    print(f"Found {total_images} images to process in database...")
    
    for root, _, files in os.walk(db_path):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(root, file)
                try:
                    # Removed the timing for single representation
                    representation = DeepFace.represent(
                        img_path=img_path,
                        model_name=MODEL_NAME,
                        detector_backend=DETECTOR_BACKEND,
                        align=True,
                        enforce_detection=False
                    )
                    
                    representations.append({
                        "identity": img_path,
                        "representation": representation[0]["embedding"]
                    })
                    processed_images += 1
                    
                    if processed_images % 10 == 0:
                        print(f"Processed {processed_images}/{total_images} images...")
                        
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")
    
    if representations:
        start_timing("saving_representations")
        timestamp = datetime.datetime.now().strftime('%Y%m%d')
        representations_file = os.path.join(db_path, f"representations.pkl")
        with open(representations_file, 'wb') as f:
            pickle.dump(representations, f)
        end_timing("saving_representations")
        
        print(f"\nRepresentation generation complete:")
        print(f"- Processed {processed_images} of {total_images} images")
        print(f"- Saved to: {representations_file}")
        
        return representations_file
    return None

def run_verification(img_path: str, exclude_path: str = None, 
                   db_path: str = os.path.join(PROJECT_DIR, 'SavedFaces', datetime.datetime.now().strftime('%Y-%m-%d')),
                   representations_file: str = None) -> dict:
    """Optimized verification function with timing measurements"""
    
    # Reset timings for this run
    global timings
    timings = {}
    
    print("\nStarting verification process...")
    
    # 1. Input face detection
    start_timing("input_face_detection")
    if not detect_face_once(img_path):
        end_timing("input_face_detection")
        print("No face detected in input.")
        return {
            "match_found": False,
            "matched_image": None,
            "distance": None,
            "verified": None,
            "raw_result": None
        }
    end_timing("input_face_detection")

    # 2. Representation finding (either pre-computed or live)
    start_timing("representation_finding")
    
    if representations_file and os.path.exists(representations_file):
        print("Using pre-computed representations...")
        try:
            with open(representations_file, 'rb') as f:
                representations = pickle.load(f)
            
            # Get representation for input image
            target_representation = DeepFace.represent(
                img_path=img_path,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR_BACKEND,
                align=True,
                enforce_detection=False
            )
            target_embedding = target_representation[0]["embedding"]
            
            # Calculate distances
            distances = []
            norm_exclude_path = os.path.normpath(exclude_path) if exclude_path else None
            
            for item in representations:
                if norm_exclude_path and (
                    item["identity"] == norm_exclude_path or
                    os.path.basename(item["identity"]) == os.path.basename(exclude_path)
                ):
                    continue
                    
                distance = cosine_distance(target_embedding, item["representation"])
                if distance <= THRESHOLD:
                    distances.append({
                        "distance": distance,
                        "identity": item["identity"]
                    })
            
            end_timing("representation_finding")
            
            if distances:
                # Sort by distance and get the best match
                distances.sort(key=lambda x: x["distance"])
                best_match = distances[0]
                
                # Verify the best match with full pipeline for confirmation
                verification_result = verify_pair((img_path, best_match["identity"]))
                if verification_result:
                    return verification_result
            
        except Exception as e:
            end_timing("representation_finding")
            print(f"Error using pre-computed representations: {e}")
            # Fall through to regular verification

    # Fallback to standard verification if no pre-computed representations or error occurred
    print("Using standard DeepFace.find...")
    try:
        dfs = DeepFace.find(
            img_path=img_path,
            db_path=db_path,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            align=True,
            enforce_detection=False,
        )
        end_timing("representation_finding")
    except Exception as e:
        end_timing("representation_finding")
        print(f"DeepFace.find failed: {e}")
        return {
            "match_found": False,
            "matched_image": None,
            "distance": None,
            "verified": None,
            "raw_result": None
        }

    if len(dfs) == 0 or dfs[0].empty:
        print("No matches found.")
        return {
            "match_found": False,
            "matched_image": None,
            "distance": None,
            "verified": None,
            "raw_result": None
        }

    # 3. Candidate verification
    start_timing("candidate_verification")
    norm_exclude_path = os.path.normpath(exclude_path) if exclude_path else None
    tasks = []
    
    for _, row in dfs[0].iterrows():
        matched_path = os.path.normpath(row["identity"])
        if norm_exclude_path and (
            matched_path == norm_exclude_path or
            os.path.basename(matched_path) == os.path.basename(exclude_path)
        ):
            continue
        tasks.append((img_path, matched_path))

    print(f"Verifying {len(tasks)} candidate matches...")

    # Run verification based on available hardware
    results = []
    try:
        if gpus:
            print("GPU detected. Running verification with ThreadPoolExecutor...")
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(verify_pair, tasks))
        else:
            print(f"Using CPU with multiprocessing across {min(cpu_count(), 8)} cores...")
            with Pool(min(cpu_count(), 8)) as pool:
                results = pool.map(verify_pair, tasks)
    except Exception as e:
        print(f"Verification failed: {e}")
        return {
            "match_found": False,
            "matched_image": None,
            "distance": None,
            "verified": None,
            "raw_result": None
        }
    
    end_timing("candidate_verification")

    # Print timing summary
    print("\nTiming Summary:")
    end_timing("input_face_detection")  # Ensure it's recorded if not already
    end_timing("representation_finding")
    end_timing("candidate_verification")
    
    total_time = sum(v for k,v in timings.items() if k not in ["face_detection", "pair_verification"])
    print(f"\nTotal verification time: {total_time:.2f} seconds")

    # Return first valid match
    for res in results:
        if res:
            return res

    return {
        "match_found": False,
        "matched_image": None,
        "distance": None,
        "verified": None,
        "raw_result": None
    }

# if __name__ == "__main__":
#     img_path = "D:/Github Repo/Visitor-Monitoring-System/SavedFaces/2025-05-04/agatha.jpg"
#     # img_path = "/content/drive/MyDrive/Colab Notebooks/test/sherwin.png"
#     exclude_path = img_path
#     saved_path = os.path.join(PROJECT_DIR, 'SavedFaces', datetime.datetime.now().strftime('%Y-%m-%d'))
#     # saved_path = os.path.join(PROJECT_DIR, 'SavedFaces')
#     # saved_path = '/content/drive/MyDrive/Colab Notebooks/test'
    
#     # Create or update representations file
#     print("Creating/updating face representations database...")
#     start_timing("total_representation_creation")
#     representations_file = create_representations_db(saved_path)
#     end_timing("total_representation_creation")
    
#     # Run verification
#     print("\nRunning face verification...")
#     start_timing("total_verification")
#     result = run_verification(
#         img_path=img_path,
#         exclude_path=exclude_path,
#         db_path=saved_path,
#         representations_file=representations_file
#     )
#     end_timing("total_verification")
    
#     # Final output
#     print("\nFinal Result:")
#     print(f"Match Found: {result['match_found']}")
#     if result['match_found']:
#         print(f"Matched Image: {result['matched_image']}")
#         print(f"Distance: {result['distance']}")
#         print(f"Verified: {result['verified']}")
    
#     print("\nTotal operation time:")
#     print(f"- Representation creation: {timings.get('total_representation_creation', 0):.2f}s")
#     print(f"- Verification process: {timings.get('total_verification', 0):.2f}s")
#     print(result)