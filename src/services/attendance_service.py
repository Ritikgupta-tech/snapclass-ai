"""
Attendance session and recognition service for SNAPCLASS AI.
Coordinates multi-modal facial and voice analysis, review structuring, and idempotent database persistence.
"""

from typing import List, Dict, Any, Tuple, Optional
import sys
import uuid
import threading
from datetime import datetime
import pandas as pd
from PIL import Image

from src.database.db import (
    get_enrolled_students_for_subject,
    create_attendance as db_create_attendance,
    get_attendance_for_teacher as db_get_attendance_for_teacher,
    check_teacher_owns_subject,
    check_attendance_session_exists
)
from src.validators.image_validators import validate_and_prepare_image
from src.validators.audio_validators import validate_audio_payload

# Lazy access to heavy ML pipelines to avoid multi-second startup overhead on page loads
def _get_analyze_classroom_photo():
    from src.pipelines.face_pipeline import analyze_classroom_photo
    return analyze_classroom_photo

def _get_process_bulk_audio():
    from src.pipelines.voice_pipeline import process_bulk_audio
    return process_bulk_audio

def __getattr__(name):
    if name == "analyze_classroom_photo":
        fn = _get_analyze_classroom_photo()
        globals()["analyze_classroom_photo"] = fn
        return fn
    if name == "process_bulk_audio":
        fn = _get_process_bulk_audio()
        globals()["process_bulk_audio"] = fn
        return fn
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# In-memory session idempotency store and thread-safe mutex
_CONFIRMED_SESSION_IDS = set()
_CONFIRM_LOCK = threading.Lock()

def prepare_face_attendance_session(
    subject_id: int,
    images: List[Image.Image],
    teacher_id: Optional[int] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Process classroom photos and generate an editable attendance review draft.
    Returns: (is_success, message, session_draft)
    """
    if teacher_id and not check_teacher_owns_subject(teacher_id, subject_id):
        return False, "Unauthorized: You do not own this academic subject.", None

    if not images:
        return False, "No classroom photos provided. Please upload or capture at least one image.", None

    # 1. Fetch only enrolled students for this subject, including face embeddings
    enrolled_students = get_enrolled_students_for_subject(subject_id, include_embeddings=True)
    if not enrolled_students:
        return False, "No students are enrolled in this subject yet. Share the subject code first.", None

    candidates_with_emb = [s for s in enrolled_students if s.get("face_embedding")]
    if not candidates_with_emb:
        return False, "Enrolled students do not have facial profiles registered. Students must enroll face biometrics.", None

    session_id = uuid.uuid4().hex[:12]
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    student_detections: Dict[int, Dict[str, Any]] = {}
    total_unknown_faces = 0
    total_faces_found = 0

    # 2. Analyze each image
    for idx, img in enumerate(images):
        photo_label = f"Photo {idx + 1}"
        is_valid, err_msg, np_img = validate_and_prepare_image(img)
        if not is_valid or np_img is None:
            continue

        analyzer = getattr(sys.modules[__name__], "analyze_classroom_photo")
        analysis = analyzer(np_img, candidates_with_emb)
        total_unknown_faces += analysis["unknown_faces"]
        total_faces_found += analysis["total_faces"]

        for sid, match_info in analysis["matches"].items():
            if sid not in student_detections:
                student_detections[sid] = {
                    "sources": [photo_label],
                    "confidence_pct": match_info["confidence_pct"],
                    "status": match_info["status"]
                }
            else:
                student_detections[sid]["sources"].append(photo_label)
                # Keep highest confidence
                if match_info["confidence_pct"] > student_detections[sid]["confidence_pct"]:
                    student_detections[sid]["confidence_pct"] = match_info["confidence_pct"]
                    student_detections[sid]["status"] = match_info["status"]

    if total_faces_found == 0:
        return False, "No faces detected in any uploaded image. Please ensure photos are clear, well-lit, and students face the camera.", None

    # 3. Assemble review table for ALL enrolled students
    review_rows = []
    attendance_records = []

    for student in enrolled_students:
        sid = student["student_id"]
        detection = student_detections.get(sid)

        if detection:
            is_present = True
            sources_str = ", ".join(detection["sources"])
            status_label = "Present" if detection["status"] == "HIGH_CONFIDENCE" else "Review Needed"
            confidence_str = f"{detection['confidence_pct']}%"
        else:
            is_present = False
            sources_str = "None"
            status_label = "Absent"
            confidence_str = "-"

        review_rows.append({
            "student_id": sid,
            "Name": student["name"],
            "Status": status_label,
            "Is Present": is_present,
            "Confidence": confidence_str,
            "Detected In": sources_str
        })

        attendance_records.append({
            "student_id": sid,
            "subject_id": subject_id,
            "timestamp": timestamp,
            "is_present": is_present
        })

    session_payload = {
        "session_id": session_id,
        "subject_id": subject_id,
        "timestamp": timestamp,
        "review_df": pd.DataFrame(review_rows),
        "attendance_records": attendance_records,
        "total_enrolled": len(enrolled_students),
        "total_faces_detected": total_faces_found,
        "unknown_faces_count": total_unknown_faces,
        "present_count": sum(1 for r in review_rows if r["Is Present"]),
        "mode": "face"
    }

    return True, "Analysis complete. Please review results below.", session_payload

def prepare_voice_attendance_session(
    subject_id: int,
    audio_bytes: bytes,
    teacher_id: Optional[int] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Process classroom audio and generate an editable attendance review draft.
    Does NOT mark all students absent if recognition fails.
    """
    if teacher_id and not check_teacher_owns_subject(teacher_id, subject_id):
        return False, "Unauthorized: You do not own this academic subject.", None

    is_valid, err_msg, duration = validate_audio_payload(audio_bytes)
    if not is_valid:
        return False, err_msg, None

    enrolled_students = get_enrolled_students_for_subject(subject_id, include_embeddings=True)
    if not enrolled_students:
        return False, "No students are enrolled in this subject.", None

    candidates_dict = {
        s["student_id"]: s.get("voice_embedding")
        for s in enrolled_students if s.get("voice_embedding")
    }

    if not candidates_dict:
        return False, "None of the enrolled students have voice profiles registered.", None

    bulk_processor = getattr(sys.modules[__name__], "process_bulk_audio")
    bulk_result = bulk_processor(audio_bytes, candidates_dict)
    if bulk_result.get("error"):
        return False, bulk_result["error"], None

    matches = bulk_result.get("matches", {})
    if not matches:
        return False, "No enrolled students were recognized in this audio recording. Please review audio or record again to avoid recording false absences.", None

    session_id = uuid.uuid4().hex[:12]
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    review_rows = []
    attendance_records = []

    for student in enrolled_students:
        sid = student["student_id"]
        match_info = matches.get(sid)

        if match_info:
            is_present = True
            status_label = "Present" if match_info["status"] == "HIGH_CONFIDENCE" else "Review Needed"
            confidence_str = f"{match_info['confidence_pct']}%"
        else:
            is_present = False
            status_label = "Absent"
            confidence_str = "-"

        review_rows.append({
            "student_id": sid,
            "Name": student["name"],
            "Status": status_label,
            "Is Present": is_present,
            "Confidence": confidence_str,
            "Detected In": "Audio Segment" if is_present else "None"
        })

        attendance_records.append({
            "student_id": sid,
            "subject_id": subject_id,
            "timestamp": timestamp,
            "is_present": is_present
        })

    session_payload = {
        "session_id": session_id,
        "subject_id": subject_id,
        "timestamp": timestamp,
        "review_df": pd.DataFrame(review_rows),
        "attendance_records": attendance_records,
        "total_enrolled": len(enrolled_students),
        "segments_processed": bulk_result.get("segments_processed", 0),
        "present_count": sum(1 for r in review_rows if r["Is Present"]),
        "mode": "voice"
    }

    return True, "Audio recognition complete. Please review attendance.", session_payload

def confirm_and_save_attendance(
    teacher_id: int,
    session_id: str,
    subject_id: int,
    final_attendance_records: List[Dict[str, Any]]
) -> Tuple[bool, str]:
    """
    Idempotently and atomically save confirmed attendance records to Supabase.
    Enforces thread-safety, payload deduplication, roster verification, and database uniqueness.
    """
    if not final_attendance_records:
        return False, "No attendance records to save."

    # 1. Thread-safe atomic in-memory lock to prevent race conditions & double-clicks
    with _CONFIRM_LOCK:
        if session_id in _CONFIRMED_SESSION_IDS:
            return False, "This attendance session has already been saved or is currently processing."
        _CONFIRMED_SESSION_IDS.add(session_id)

    # 2. Database-level persistence check (survives app restarts)
    ref_timestamp = final_attendance_records[0].get("timestamp")
    if ref_timestamp and check_attendance_session_exists(subject_id, ref_timestamp):
        with _CONFIRM_LOCK:
            _CONFIRMED_SESSION_IDS.discard(session_id)
        return False, "Attendance for this subject and session timestamp has already been recorded in the database."

    # 3. Validate teacher ownership of subject
    if not check_teacher_owns_subject(teacher_id, subject_id):
        with _CONFIRM_LOCK:
            _CONFIRMED_SESSION_IDS.discard(session_id)
        return False, "Unauthorized: You do not own this subject."

    # 4. Deduplicate final_attendance_records by student_id to prevent duplicates in payload
    deduped_records: List[Dict[str, Any]] = []
    seen_student_ids = set()

    for rec in final_attendance_records:
        sid = rec.get("student_id")
        if sid is not None and sid not in seen_student_ids:
            seen_student_ids.add(sid)
            deduped_records.append({
                "student_id": sid,
                "subject_id": subject_id,
                "timestamp": rec.get("timestamp") or ref_timestamp,
                "is_present": bool(rec.get("is_present", False))
            })

    # 5. Verify student IDs belong to enrolled roster (server-side authorization)
    enrolled = get_enrolled_students_for_subject(subject_id, include_embeddings=False)
    if enrolled:
        enrolled_ids = {s["student_id"] for s in enrolled}
        invalid_sids = [r["student_id"] for r in deduped_records if r["student_id"] not in enrolled_ids]
        if invalid_sids:
            with _CONFIRM_LOCK:
                _CONFIRMED_SESSION_IDS.discard(session_id)
            return False, f"Cannot record attendance: Student ID(s) {invalid_sids} are not enrolled in this subject."

    try:
        saved_logs = db_create_attendance(deduped_records)
        if saved_logs:
            return True, f"Successfully confirmed attendance for {len(saved_logs)} students!"
        with _CONFIRM_LOCK:
            _CONFIRMED_SESSION_IDS.discard(session_id)
        return False, "Database returned empty result during save."
    except Exception as e:
        err_str = str(e).lower()
        # Translate PostgreSQL unique constraint / duplicate key violations gracefully
        if "23505" in err_str or "duplicate key" in err_str or "unique constraint" in err_str:
            return False, "Attendance for this subject and session timestamp has already been recorded in the database."
        with _CONFIRM_LOCK:
            _CONFIRMED_SESSION_IDS.discard(session_id)
        return False, f"Failed to commit attendance: {str(e)}"

def get_teacher_attendance_overview(teacher_id: int) -> List[Dict[str, Any]]:
    """
    Fetch and format attendance history for a teacher, aggregated by distinct sessions.
    """
    raw_records = db_get_attendance_for_teacher(teacher_id)
    if not raw_records:
        return []

    # Group records by (timestamp, subject_id)
    session_groups: Dict[Tuple[str, int], Dict[str, Any]] = {}

    for r in raw_records:
        ts = r.get("timestamp") or ""
        sub = r.get("subjects") or {}
        sid = sub.get("subject_id") or r.get("subject_id")
        key = (ts, sid)

        if key not in session_groups:
            # Parse human-readable date
            try:
                dt_obj = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                formatted_time = dt_obj.strftime("%b %d, %Y - %I:%M %p")
            except Exception:
                formatted_time = ts

            session_groups[key] = {
                "timestamp": ts,
                "formatted_time": formatted_time,
                "subject_name": sub.get("name", "Unknown"),
                "subject_code": sub.get("subject_code", "N/A"),
                "section": sub.get("section", "N/A"),
                "total_students": 0,
                "present_count": 0,
                "records": []
            }

        session_groups[key]["total_students"] += 1
        if r.get("is_present"):
            session_groups[key]["present_count"] += 1
        session_groups[key]["records"].append(r)

    # Convert to formatted list sorted by timestamp descending
    results = list(session_groups.values())
    for item in results:
        tot = item["total_students"]
        pres = item["present_count"]
        item["attendance_rate"] = f"{round((pres / tot * 100), 1)}%" if tot > 0 else "0.0%"
        item["summary_badge"] = f"{pres} / {tot} Present ({item['attendance_rate']})"

    return sorted(results, key=lambda x: x["timestamp"], reverse=True)
