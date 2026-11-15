"""
Subject and enrollment service for SNAPCLASS AI.
Handles subject creation, validation, duplicate prevention, QR share generation, and student enrollment.
"""

from typing import Tuple, Optional, Dict, Any, List
import io
import segno
from src.database.db import (
    create_subject as db_create_subject,
    get_teacher_subjects as db_get_teacher_subjects,
    get_subject_by_code as db_get_subject_by_code,
    get_subject_by_id as db_get_subject_by_id,
    enroll_student_to_subject as db_enroll_student,
    unenroll_student_to_subject as db_unenroll_student,
    get_student_subjects as db_get_student_subjects,
    get_student_attendance as db_get_student_attendance,
    get_enrolled_students_for_subject
)
from src.validators.input_validators import validate_subject_inputs
from src.config.app_config import CANONICAL_APP_URL

def create_new_subject(
    teacher_id: int,
    subject_code: str,
    name: str,
    section: str
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Validate and create a new course subject.
    Prevents duplicate subject codes.
    """
    is_valid, err_msg = validate_subject_inputs(subject_code, name, section)
    if not is_valid:
        return False, err_msg, None

    clean_code = subject_code.strip().upper()

    # Check for existing code collision
    existing = db_get_subject_by_code(clean_code)
    if existing:
        return False, f"Subject code '{clean_code}' is already taken. Please choose a distinct code.", None

    try:
        created = db_create_subject(clean_code, name.strip(), section.strip(), teacher_id)
        if created and len(created) > 0:
            return True, f"Subject '{name.strip()}' ({clean_code}) created successfully!", created[0]
        return False, "Failed to create subject in database.", None
    except Exception as e:
        return False, f"Database error creating subject: {str(e)}", None

def enroll_student_by_code(
    student_id: int,
    subject_code: str
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Enroll student into a subject using subject code.
    Prevents duplicate enrollments.
    """
    clean_code = (subject_code or "").strip().upper()
    if not clean_code:
        return False, "Subject code cannot be empty.", None

    subject = db_get_subject_by_code(clean_code)
    if not subject:
        return False, f"No subject found with code '{clean_code}'.", None

    subject_id = subject["subject_id"]

    try:
        res = db_enroll_student(student_id, subject_id)
        return True, f"Successfully enrolled in {subject['name']} ({clean_code})!", subject
    except Exception as e:
        return False, f"Enrollment error: {str(e)}", None

def unenroll_student_from_subject(
    student_id: int,
    subject_id: int
) -> Tuple[bool, str]:
    """Remove student enrollment from a subject."""
    try:
        db_unenroll_student(student_id, subject_id)
        return True, "Successfully unenrolled from the course."
    except Exception as e:
        return False, f"Failed to unenroll: {str(e)}"

def get_student_dashboard_data(student_id: int) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Fetch all enrolled subjects for a student alongside attendance statistics.
    Returns: (subjects_list, overall_stats)
    """
    enrolled_nodes = db_get_student_subjects(student_id)
    attendance_records = db_get_student_attendance(student_id)

    # Map attendance by subject_id
    stats_map: Dict[int, Dict[str, int]] = {}
    total_attended_overall = 0
    total_classes_overall = len(attendance_records)

    for record in attendance_records:
        sid = record.get("subject_id")
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if record.get("is_present"):
            stats_map[sid]["attended"] += 1
            total_attended_overall += 1

    formatted_subjects = []
    for node in enrolled_nodes:
        sub = node.get("subjects")
        if not sub:
            continue
        sid = sub.get("subject_id")
        sub_stats = stats_map.get(sid, {"total": 0, "attended": 0})
        pct = round((sub_stats["attended"] / sub_stats["total"] * 100), 1) if sub_stats["total"] > 0 else 0.0

        formatted_subjects.append({
            "subject_id": sid,
            "subject_code": sub.get("subject_code"),
            "name": sub.get("name"),
            "section": sub.get("section"),
            "total_classes": sub_stats["total"],
            "attended_classes": sub_stats["attended"],
            "attendance_pct": pct
        })

    overall_pct = round((total_attended_overall / total_classes_overall * 100), 1) if total_classes_overall > 0 else 0.0
    overall_summary = {
        "enrolled_count": len(formatted_subjects),
        "total_classes": total_classes_overall,
        "total_attended": total_attended_overall,
        "overall_pct": overall_pct
    }

    return formatted_subjects, overall_summary

def generate_qr_share_details(subject_name: str, subject_code: str) -> Dict[str, Any]:
    """
    Generate canonical join URL and high-resolution QR code PNG bytes.
    """
    clean_code = subject_code.strip().upper()
    join_url = f"{CANONICAL_APP_URL}/?join-code={clean_code}"

    qr = segno.make(join_url, error="h")
    out = io.BytesIO()
    qr.save(out, kind="png", scale=8, border=2)

    return {
        "join_url": join_url,
        "subject_code": clean_code,
        "subject_name": subject_name,
        "qr_png_bytes": out.getvalue()
    }
