from deepface import DeepFace
from retinaface import RetinaFace
import pandas as pd
import os
import concurrent.futures

# STATIC THRESHOLD (per Sher1)
THRESHOLD = 0.56

def detect_face(image_path):
    detections = RetinaFace.detect_faces(image_path)
    return bool(detections)

def run_verification(img_path: str, db_path: str = "./SavedFaces", exclude_path: str = None) -> dict:
    """
    Perform face detection and verification using DeepFace + RetinaFace.
    
    Args:
        img_path (str): Path to the image to verify.
        db_path (str): Path to the image database directory.
        exclude_path (str): Path to exclude from comparison (to avoid self-matching).
    
    Returns:
        dict: {
            'match_found': bool,
            'matched_image': str or None,
            'distance': float or None,
            'verified': bool or None,
            'raw_result': dict
        }
    """
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
        detector_backend="retinaface",
        align=True
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

    # Prepare candidate matches, skipping self-matches
    candidates = []
    for index, row in dfs[0].iterrows():
        matched_img_path = row["identity"]
        norm_matched_path = os.path.normpath(matched_img_path)
        if (norm_exclude_path and norm_matched_path == norm_exclude_path) or \
           (exclude_path and os.path.basename(matched_img_path) == os.path.basename(exclude_path)):
            continue
        candidates.append(matched_img_path)

    def process_candidate(matched_img_path):
        if detect_face(matched_img_path):
            result = DeepFace.verify(
                img1_path=img_path,
                img2_path=matched_img_path,
                model_name="ArcFace",
                detector_backend="retinaface",
                align=True
            )
            distance = result.get("distance", 1.0)
            match_found = distance <= THRESHOLD
            return {
                "match_found": match_found,
                "matched_image": matched_img_path,
                "distance": distance,
                "verified": result.get("verified"),
                "raw_result": result
            }
        return None

    # Use ThreadPoolExecutor to process candidates in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_candidate = {executor.submit(process_candidate, c): c for c in candidates}
        for future in concurrent.futures.as_completed(future_to_candidate):
            result = future.result()
            if result and result["match_found"]:
                print(f"Match: {img_path} matches with {result['matched_image']}")
                return result
            elif result:
                print(f"No Match: {img_path} does not match {result['matched_image']}")

    # No valid matches with detectable faces
    return {
        "match_found": False,
        "matched_image": None,
        "distance": None,
        "verified": None,
        "raw_result": None
    }