from deepface import DeepFace
from retinaface import RetinaFace
import pandas as pd
import os
import datetime
import time

# STATIC THRESHOLD (per Sher1)
THRESHOLD = 0.70
image_path = "./SavedFaces/2025-05-03/cholo3.png"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def detect_face(image_path):
    detections = RetinaFace.detect_faces(image_path)
    return bool(detections)

def run_verification(img_path: str, db_path: str = "./SavedFaces/2025-05-03") -> dict:
    """
    Perform face detection and verification using DeepFace + RetinaFace.
    
    Args:
        img_path (str): Path to the image to verify.
        db_path (str): Path to the image database directory.
    
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

    print("Face detected in the original image.")

    # Search for potential matches
    dfs = DeepFace.find(
        img_path=img_path,
        db_path=db_path,
        model_name="ArcFace",
        detector_backend="retinaface",
        align=True
    )
    print(dfs)

    if len(dfs) == 0 or dfs[0].empty:
        print("No matching image found in the database.")
        return {
            "match_found": False,
            "matched_image": None,
            "distance": None,
            "verified": None,
            "raw_result": None
        }

    # Iterate through closest matches
    for index, row in dfs[0].iterrows():
        matched_img_path = row["identity"]
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

if __name__ == "__main__":
    img_path = "D:/Merrell/Visitor-Monitoring-System/SavedFaces/2025-05-03/osh2.jpg"
    # img_path = "/content/drive/MyDrive/Colab Notebooks/test/sherwin.png"
    exclude_path = img_path
    #saved_path = "D:/Merrell/Visitor-Monitoring-System/SavedFaces/2025-05-03"
    saved_path = os.path.join(PROJECT_DIR, 'SavedFaces', datetime.datetime.now().strftime('%Y-%m-%d'))
    # saved_path = '/content/drive/MyDrive/Colab Notebooks/test'
    
    result = run_verification(img_path, saved_path)
    print("Verification completed.", result)