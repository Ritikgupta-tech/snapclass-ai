"""
Database Access Layer for SNAPCLASS AI.
Provides hardened queries, safe column selection, and referential validation.
"""

from typing import List, Dict, Any, Optional
import bcrypt
import logging
from src.database.config import supabase

logger = logging.getLogger(__name__)

# --- Cryptographic Helpers ---

def hash_pass(pwd: str) -> str:
    """Hash password using bcrypt with salt."""
    return bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pass(pwd: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(pwd.encode('utf-8'), hashed.encode('utf-8'))
    except Exception as e:
        logger.error(f"Error checking password hash: {e}")
        return False

# --- Teacher Operations ---

def check_teacher_exists(username: str) -> bool:
    """Check if a teacher with the given username already exists."""
    clean_username = username.strip().lower()
    response = supabase.table("teachers").select("teacher_id").eq("username", clean_username).execute()
    return bool(response.data and len(response.data) > 0)

def create_teacher(username: str, password: str, name: str) -> Optional[Dict[str, Any]]:
    """Create a new teacher record."""
    clean_username = username.strip().lower()
    clean_name = name.strip()
    data = {
        "username": clean_username,
        "password": hash_pass(password),
        "name": clean_name
    }
    response = supabase.table("teachers").insert(data).execute()
    if response.data and len(response.data) > 0:
        teacher = response.data[0]
        # Never leak password hash to callers
        teacher.pop("password", None)
        return teacher
    return None

def teacher_login(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate teacher credentials.
    Returns safe teacher dict without password hash on success, or None on failure.
    """
    clean_username = username.strip().lower()
    response = supabase.table("teachers").select("teacher_id, username, password, name").eq("username", clean_username).execute()
    if response.data and len(response.data) > 0:
        teacher = response.data[0]
        if check_pass(password, teacher.get("password", "")):
            # Secure: remove password hash before returning to session state
            teacher.pop("password", None)
            return teacher
    return None

def get_teacher_by_id(teacher_id: int) -> Optional[Dict[str, Any]]:
    """Fetch safe teacher profile by ID."""
    response = supabase.table("teachers").select("teacher_id, username, name").eq("teacher_id", teacher_id).execute()
    return response.data[0] if response.data else None

# --- Student Operations ---

def get_all_students(include_embeddings: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch all students. By default, omits heavy biometric embeddings
    to prevent memory bloat and sensitive data exposure.
    """
    columns = "student_id, name, face_embedding, voice_embedding" if include_embeddings else "student_id, name"
    response = supabase.table("students").select(columns).execute()
    return response.data or []

def get_student_by_id(student_id: int, include_embeddings: bool = False) -> Optional[Dict[str, Any]]:
    """Fetch student by ID with or without embeddings."""
    columns = "student_id, name, face_embedding, voice_embedding" if include_embeddings else "student_id, name"
    response = supabase.table("students").select(columns).eq("student_id", student_id).execute()
    return response.data[0] if response.data else None

def create_student(new_name: str, face_embedding: Optional[List[float]] = None, voice_embedding: Optional[List[float]] = None) -> List[Dict[str, Any]]:
    """Register a new student with biometric vectors."""
    data = {
        "name": new_name.strip(),
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }
    response = supabase.table("students").insert(data).execute()
    # Strip embeddings from return data for safe state management
    if response.data:
        for s in response.data:
            s.pop("face_embedding", None)
            s.pop("voice_embedding", None)
    return response.data or []

# --- Subject Operations ---

def get_subject_by_code(subject_code: str) -> Optional[Dict[str, Any]]:
    """Fetch subject record by subject code."""
    clean_code = subject_code.strip().upper()
    response = supabase.table("subjects").select("subject_id, subject_code, name, section, teacher_id").eq("subject_code", clean_code).execute()
    return response.data[0] if response.data else None

def get_subject_by_id(subject_id: int) -> Optional[Dict[str, Any]]:
    """Fetch subject record by primary key."""
    response = supabase.table("subjects").select("subject_id, subject_code, name, section, teacher_id").eq("subject_id", subject_id).execute()
    return response.data[0] if response.data else None

def create_subject(subject_code: str, name: str, section: str, teacher_id: int) -> List[Dict[str, Any]]:
    """Create a new subject assigned to a teacher."""
    data = {
        "subject_code": subject_code.strip().upper(),
        "name": name.strip(),
        "section": section.strip(),
        "teacher_id": teacher_id
    }
    response = supabase.table("subjects").insert(data).execute()
    return response.data or []

def get_teacher_subjects(teacher_id: int) -> List[Dict[str, Any]]:
    """
    Fetch all subjects created by a specific teacher, along with total student enrollment count
    and distinct attendance sessions.
    """
    response = supabase.table("subjects").select(
        "subject_id, subject_code, name, section, teacher_id, subject_students(count), attendance_logs(timestamp)"
    ).eq("teacher_id", teacher_id).order("subject_id", desc=True).execute()

    subjects = response.data or []

    for sub in subjects:
        # Calculate total enrolled students
        sub_students = sub.get("subject_students")
        if sub_students and len(sub_students) > 0 and isinstance(sub_students[0], dict):
            sub["total_students"] = sub_students[0].get("count", 0)
        else:
            sub["total_students"] = 0

        # Calculate distinct class sessions from logs
        attendance = sub.get("attendance_logs", [])
        unique_sessions = len(set(log.get("timestamp") for log in attendance if log.get("timestamp")))
        sub["total_classes"] = unique_sessions

        # Clean internal joined fields
        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

    return subjects

def check_teacher_owns_subject(teacher_id: int, subject_id: int) -> bool:
    """Verify that a subject belongs to the specified teacher."""
    response = supabase.table("subjects").select("subject_id").eq("subject_id", subject_id).eq("teacher_id", teacher_id).execute()
    return bool(response.data and len(response.data) > 0)

# --- Enrollment Operations ---

def enroll_student_to_subject(student_id: int, subject_id: int) -> List[Dict[str, Any]]:
    """Enroll a student in a subject."""
    # Check if already enrolled to prevent duplicate key error
    existing = supabase.table("subject_students").select("subject_id").eq("subject_id", subject_id).eq("student_id", student_id).execute()
    if existing.data and len(existing.data) > 0:
        return existing.data

    data = {"student_id": student_id, "subject_id": subject_id}
    response = supabase.table("subject_students").insert(data).execute()
    return response.data or []

def unenroll_student_to_subject(student_id: int, subject_id: int) -> List[Dict[str, Any]]:
    """Unenroll a student from a subject."""
    response = supabase.table("subject_students").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
    return response.data or []

def get_student_subjects(student_id: int) -> List[Dict[str, Any]]:
    """Fetch all subjects a student is enrolled in."""
    response = supabase.table("subject_students").select(
        "subject_id, student_id, subjects(subject_id, subject_code, name, section, teacher_id)"
    ).eq("student_id", student_id).execute()
    return response.data or []

def get_enrolled_students_for_subject(subject_id: int, include_embeddings: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch all students enrolled in a specific subject.
    Optionally include biometric embeddings for attendance pipeline execution.
    """
    student_cols = "student_id, name, face_embedding, voice_embedding" if include_embeddings else "student_id, name"
    response = supabase.table("subject_students").select(
        f"subject_id, student_id, students({student_cols})"
    ).eq("subject_id", subject_id).execute()

    enrolled = []
    for row in (response.data or []):
        student = row.get("students")
        if student:
            enrolled.append(student)
    return enrolled

# --- Attendance Operations ---

def create_attendance(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Insert attendance log records."""
    if not logs:
        return []
    response = supabase.table("attendance_logs").insert(logs).execute()
    return response.data or []

def get_student_attendance(student_id: int) -> List[Dict[str, Any]]:
    """Fetch attendance history for a student."""
    response = supabase.table("attendance_logs").select(
        "id, timestamp, subject_id, student_id, is_present, subjects(subject_id, subject_code, name, section)"
    ).eq("student_id", student_id).order("timestamp", desc=True).execute()
    return response.data or []

def get_attendance_for_teacher(teacher_id: int) -> List[Dict[str, Any]]:
    """Fetch all attendance records across subjects taught by a teacher."""
    response = supabase.table("attendance_logs").select(
        "id, timestamp, subject_id, student_id, is_present, subjects!inner(subject_id, subject_code, name, section, teacher_id), students(student_id, name)"
    ).eq("subjects.teacher_id", teacher_id).order("timestamp", desc=True).execute()
    return response.data or []
