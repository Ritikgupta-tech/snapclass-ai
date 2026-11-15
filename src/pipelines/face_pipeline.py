"""
Facial recognition pipeline for SNAPCLASS AI.
Uses dlib 128-dimensional deep metric embeddings with subject-scoped candidate matching.
"""

from typing import List, Dict, Tuple, Any, Optional
import dlib
import numpy as np
import face_recognition_models
import streamlit as st
import logging

from src.config.app_config import (
    FACE_DISTANCE_THRESHOLD,
    FACE_AMBIGUOUS_THRESHOLD,
    FACE_DETECTION_UPSAMPLE
)

logger = logging.getLogger(__name__)

@st.cache_resource
def load_dlib_models():
    """
    Load pre-trained dlib face detector, shape predictor, and recognition network.
    Cached as a process-level resource to avoid reloading 100MB+ models on reruns.
    """
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec

def get_face_embeddings(image_np: np.ndarray) -> List[np.ndarray]:
    """
    Detect all faces in an RGB image and compute 128-d metric face embeddings.
    Returns: List of numpy arrays, each of shape (128,).
    """
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, FACE_DETECTION_UPSAMPLE)

    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor, dtype=np.float64))
    return encodings

def match_face_to_candidates(
    face_encoding: np.ndarray,
    candidates: List[Dict[str, Any]],
    distance_threshold: float = FACE_DISTANCE_THRESHOLD,
    ambiguous_threshold: float = FACE_AMBIGUOUS_THRESHOLD
) -> Tuple[Optional[int], Optional[str], float, str]:
    """
    Compare a single 128-d face encoding against a list of candidate student dicts.
    Each candidate should have: 'student_id', 'name', and 'face_embedding'.

    Returns: (best_student_id, best_student_name, min_distance, status)
    where status is 'HIGH_CONFIDENCE', 'NEEDS_REVIEW', or 'UNKNOWN'.
    """
    if not candidates:
        return None, None, 1.0, "UNKNOWN"

    best_sid = None
    best_name = None
    min_dist = float("inf")
    second_min_dist = float("inf")

    for cand in candidates:
        embedding = cand.get("face_embedding")
        if not embedding:
            continue

        cand_vector = np.array(embedding, dtype=np.float64)
        if cand_vector.shape != (128,):
            continue

        # dlib face embeddings are normalized metric embeddings; Euclidean distance is canonical
        dist = float(np.linalg.norm(cand_vector - face_encoding))

        if dist < min_dist:
            second_min_dist = min_dist
            min_dist = dist
            best_sid = cand.get("student_id")
            best_name = cand.get("name")
        elif dist < second_min_dist:
            second_min_dist = dist

    # If top candidate and runner-up candidate have very close distances (e.g. twins or similar features),
    # downgrade to NEEDS_REVIEW to prevent false student attribution
    if (second_min_dist - min_dist) < 0.05 and min_dist <= distance_threshold:
        return best_sid, best_name, min_dist, "NEEDS_REVIEW"

    if min_dist <= distance_threshold:
        return best_sid, best_name, min_dist, "HIGH_CONFIDENCE"
    elif min_dist <= ambiguous_threshold:
        return best_sid, best_name, min_dist, "NEEDS_REVIEW"
    else:
        return None, None, min_dist, "UNKNOWN"

def analyze_classroom_photo(
    image_np: np.ndarray,
    enrolled_candidates: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Analyze a classroom photo against enrolled candidates of the current subject.
    Identifies high confidence matches, ambiguous matches, and unknown faces.

    Returns dict with:
      - 'matches': dict[student_id -> {name, distance, status, count}]
      - 'unknown_faces': int
      - 'total_faces': int
    """
    encodings = get_face_embeddings(image_np)
    matches: Dict[int, Dict[str, Any]] = {}
    unknown_count = 0

    for enc in encodings:
        sid, name, dist, status = match_face_to_candidates(enc, enrolled_candidates)
        if status in ("HIGH_CONFIDENCE", "NEEDS_REVIEW") and sid is not None:
            if sid not in matches or dist < matches[sid]["distance"]:
                matches[sid] = {
                    "student_id": sid,
                    "name": name,
                    "distance": round(dist, 4),
                    "status": status,
                    "confidence_pct": round(max(0.0, min(100.0, (1.0 - (dist / FACE_AMBIGUOUS_THRESHOLD)) * 100)), 1)
                }
        else:
            unknown_count += 1

    return {
        "matches": matches,
        "unknown_faces": unknown_count,
        "total_faces": len(encodings)
    }

# Backward compatibility helper for student face login
def predict_attendance(class_image_np: np.ndarray) -> Tuple[Dict[int, bool], List[int], int]:
    """
    Legacy compatibility wrapper for student FaceID login.
    Detects face and checks against all enrolled students in database.
    """
    from src.database.db import get_all_students
    encodings = get_face_embeddings(class_image_np)
    detected_student: Dict[int, bool] = {}

    all_students_db = get_all_students(include_embeddings=True)
    all_student_ids = [s["student_id"] for s in all_students_db]

    for enc in encodings:
        sid, _, dist, status = match_face_to_candidates(
            enc, all_students_db,
            distance_threshold=0.55,
            ambiguous_threshold=0.62
        )
        if sid and status in ("HIGH_CONFIDENCE", "NEEDS_REVIEW"):
            detected_student[sid] = True

    return detected_student, all_student_ids, len(encodings)

def train_classifier():
    """No-op retained for backwards compatibility without flushing model weights."""
    return True
