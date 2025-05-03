from deepface import DeepFace
from retinaface import RetinaFace
import pandas as pd
import os
import datetime
import tensorflow as tf

# Enable GPU memory growth (prevents TensorFlow from allocating all GPU memory at once)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"Using GPU(s): {[gpu.name for gpu in gpus]}")
    except RuntimeError as e:
        print(e)
else:
    print("No GPU detected. Running on CPU.")

# STATIC THRESHOLD (per Sher1)
THRESHOLD = 0.56

def detect_face(image_path):
    detections = RetinaFace.detect_faces(image_path)
    return bool(detections)

project_dir = os.path.dirname(os.path.abspath(__file__))
saved_path = os.path.join(project_dir, 'SavedFaces', datetime.datetime.now().strftime('%Y-%m-%d'))

def run_verification(img_path: str, exclude_path: str = None, db_path: str = saved_path) -> dict:
    # Check for GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"GPU detected: {gpus[0].name}")
        detector = 'retinaface'  # Use RetinaFace for GPU
    else:
        print("No GPU detected. Running on CPU.")
        detector = 'opencv'

    if not detect_face(img_path):
        print("No face detected in the original image.")
        return {
            "match_found": False,
            "matched_image": None,
            "distance": None,
            "verified": None,
            "raw_result": None
        }

    print(f"Face detected in the original image: {img_path}")
    print(f"Exclude path: {exclude_path}")

    # Normalize paths for comparison
    norm_img_path = os.path.normpath(img_path)
    norm_exclude_path = os.path.normpath(exclude_path) if exclude_path else None
    
    print(f"Normalized paths - Image: {norm_img_path}, Exclude: {norm_exclude_path}")

    # Search for potential matches
    dfs = DeepFace.find(
        img_path=img_path,
        db_path=db_path,
        model_name="ArcFace",
        detector_backend=detector,  # Changed from 'retinaface' to 'opencv'
        align=True,
        enforce_detection=False
    )
    
    if len(dfs) == 0 or dfs[0].empty:
        print("No matching image found in the database.")
        return {
            "match_found": False,
            "matched_image": None,
            "distance": None,
            "verified": None,
            "raw_result": None
        }

    print(f"Found {len(dfs[0])} potential matches")
    
    # Iterate through closest matches
    for index, row in dfs[0].iterrows():
        matched_img_path = row["identity"]
        norm_matched_path = os.path.normpath(matched_img_path)
        
        # Skip if this is the image we're comparing against (to avoid self-matching)
        if norm_exclude_path and norm_matched_path == norm_exclude_path:
            print(f"Skipping self-match: {matched_img_path}")
            continue
            
        # Also check by filename as a fallback
        if exclude_path and os.path.basename(matched_img_path) == os.path.basename(exclude_path):
            print(f"Skipping self-match by filename: {matched_img_path}")
            continue
            
        if detect_face(matched_img_path):
            print(f"Face detected in matched image: {matched_img_path}")
            result = DeepFace.verify(
                img1_path=img_path,
                img2_path=matched_img_path,
                model_name="ArcFace",
                detector_backend=detector,  # Changed from 'retinaface' to 'opencv'
                align=True
            )
            print("Verification Result:", result)

            distance = result.get("distance", 1.0)
            match_found = distance <= THRESHOLD

            if match_found:
                print(f"Match: {img_path} matches with {matched_img_path}")
            else:
                print(f"No Match: {img_path} does not match {matched_img_path}")

            return {
                "match_found": match_found,
                "matched_image": matched_img_path,
                "distance": distance,
                "verified": result.get("verified"),
                "raw_result": result
            }
        else:
            print(f"No face detected in {matched_img_path}, trying next match...")

    # No valid matches with detectable faces
    return {
        "match_found": False,
        "matched_image": None,
        "distance": None,
        "verified": None,
        "raw_result": None
    }


if __name__ == "__main__":
    # Check for GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"GPU detected: {gpus[0].name}")
    else:
        print("No GPU detected. Running on CPU.")

    # Example usage
    img_path = "D:/Github Repo/Visitor-Monitoring-System/SavedFaces/2025-05-03/cholo.jpg"
    project_dir = os.path.dirname(os.path.abspath(__file__))
    saved_path = os.path.join(project_dir, 'SavedFaces', datetime.datetime.now().strftime('%Y-%m-%d'))
    # saved_path = os.path.join(project_dir, 'SavedFaces', '2025-05-03')
    print("Saved Path:", saved_path)
    exclude_path = img_path  # Optional

    result = run_verification(img_path=img_path, exclude_path=exclude_path, db_path=saved_path)
    print("Final Result:", result)