from deepface import DeepFace
from retinaface import RetinaFace
import pandas as pd

# STATIC THRESHOLD (per Sher1)
THRESHOLD = 0.57

def detect_face(image_path):
    detections = RetinaFace.detect_faces(image_path)
    return bool(detections)

def run_verification(img_path: str, db_path: str = "./SavedFaces") -> dict:
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
