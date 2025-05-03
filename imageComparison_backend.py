from deepface import DeepFace
from retinaface import RetinaFace
import pandas as pd
import os

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
                detector_backend="retinaface",
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