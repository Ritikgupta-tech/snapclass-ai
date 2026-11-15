"""
Authentication and session security service for SNAPCLASS AI.
Handles credential verification, password policy enforcement, rate limiting, and clean session termination.
"""

from typing import Tuple, Optional, Dict, Any
import time
import threading
import streamlit as st
from src.database.db import (
    teacher_login as db_teacher_login,
    create_teacher as db_create_teacher,
    check_teacher_exists,
    get_student_by_id,
    create_student as db_create_student
)
from src.validators.input_validators import (
    validate_username,
    validate_password
)
from src.config.app_config import MAX_LOGIN_ATTEMPTS, LOCKOUT_DURATION_SECONDS

# Module-level persistent tracker across all Streamlit sessions in this process.
# Thread-safe in-memory rate limiting; protects against session-clearing & tab resets.
_GLOBAL_LOGIN_ATTEMPTS: Dict[str, Dict[str, Any]] = {}
_LOGIN_LOCK = threading.Lock()

def _get_client_ip() -> str:
    """Safely extract client IP from Streamlit context without raising outside request."""
    try:
        return getattr(st.context, "ip_address", None) or "local"
    except Exception:
        return "local"

def _get_login_attempts() -> Dict[str, Dict[str, Any]]:
    """Retrieve process-wide rate limiting attempt tracker."""
    global _GLOBAL_LOGIN_ATTEMPTS
    return _GLOBAL_LOGIN_ATTEMPTS

def _is_rate_limited(username: str, ip: Optional[str] = None) -> Tuple[bool, int]:
    """Check if username or client IP is temporarily locked out due to excessive failed attempts."""
    now = time.time()
    with _LOGIN_LOCK:
        # 1. Check target username limit
        record = _GLOBAL_LOGIN_ATTEMPTS.get(username)
        if record:
            attempts = record.get("count", 0)
            elapsed = now - record.get("last_attempt", 0)
            if attempts >= MAX_LOGIN_ATTEMPTS:
                if elapsed < LOCKOUT_DURATION_SECONDS:
                    return True, int(LOCKOUT_DURATION_SECONDS - elapsed)
                else:
                    _GLOBAL_LOGIN_ATTEMPTS[username] = {"count": 0, "last_attempt": now}

        # 2. Check client IP limit (protects against distributed dictionary spraying)
        if ip and ip != "local":
            ip_key = f"ip:{ip}"
            ip_record = _GLOBAL_LOGIN_ATTEMPTS.get(ip_key)
            if ip_record:
                ip_attempts = ip_record.get("count", 0)
                ip_elapsed = now - ip_record.get("last_attempt", 0)
                if ip_attempts >= (MAX_LOGIN_ATTEMPTS * 3):
                    if ip_elapsed < LOCKOUT_DURATION_SECONDS:
                        return True, int(LOCKOUT_DURATION_SECONDS - ip_elapsed)
                    else:
                        _GLOBAL_LOGIN_ATTEMPTS[ip_key] = {"count": 0, "last_attempt": now}

    return False, 0

def _record_failed_attempt(username: str, ip: Optional[str] = None):
    """Increment failed login attempts for rate limiting."""
    now = time.time()
    with _LOGIN_LOCK:
        rec = _GLOBAL_LOGIN_ATTEMPTS.get(username, {"count": 0, "last_attempt": now})
        rec["count"] += 1
        rec["last_attempt"] = now
        _GLOBAL_LOGIN_ATTEMPTS[username] = rec

        if ip and ip != "local":
            ip_key = f"ip:{ip}"
            ip_rec = _GLOBAL_LOGIN_ATTEMPTS.get(ip_key, {"count": 0, "last_attempt": now})
            ip_rec["count"] += 1
            ip_rec["last_attempt"] = now
            _GLOBAL_LOGIN_ATTEMPTS[ip_key] = ip_rec

def _clear_failed_attempts(username: str, ip: Optional[str] = None):
    """Clear failed attempts upon successful authentication."""
    with _LOGIN_LOCK:
        _GLOBAL_LOGIN_ATTEMPTS.pop(username, None)
        if ip and ip != "local":
            _GLOBAL_LOGIN_ATTEMPTS.pop(f"ip:{ip}", None)

def login_teacher(username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Authenticate teacher with rate-limiting and safe session population.
    Returns: (is_success, message, safe_teacher_dict)
    """
    clean_user = (username or "").strip().lower()
    if not clean_user or not password:
        return False, "Username and password are required.", None

    client_ip = _get_client_ip()
    is_limited, remaining_sec = _is_rate_limited(clean_user, client_ip)
    if is_limited:
        return False, f"Too many failed attempts. Account temporarily locked for {remaining_sec} seconds.", None

    teacher = db_teacher_login(clean_user, password)
    if not teacher:
        _record_failed_attempt(clean_user, client_ip)
        return False, "Invalid username or password.", None

    _clear_failed_attempts(clean_user, client_ip)
    # Populate authenticated state
    st.session_state.is_logged_in = True
    st.session_state.user_role = "teacher"
    st.session_state.teacher_data = teacher

    return True, "Login successful.", teacher

def register_teacher(
    username: str,
    name: str,
    password: str,
    confirm_password: str
) -> Tuple[bool, str]:
    """
    Register a new teacher with robust format and complexity validation.
    Returns: (is_success, message)
    """
    # 1. Validate username
    is_valid_user, user_err = validate_username(username)
    if not is_valid_user:
        return False, user_err

    # 2. Validate full name
    clean_name = (name or "").strip()
    if len(clean_name) < 2 or len(clean_name) > 60:
        return False, "Full name must be between 2 and 60 characters."

    # 3. Check password matching
    if password != confirm_password:
        return False, "Passwords do not match."

    # 4. Validate password complexity
    is_valid_pass, pass_err = validate_password(password)
    if not is_valid_pass:
        return False, pass_err

    # 5. Check uniqueness
    clean_user = username.strip().lower()
    if check_teacher_exists(clean_user):
        return False, "This username is already registered. Please choose another or login."

    try:
        created = db_create_teacher(clean_user, password, clean_name)
        if created:
            return True, "Account successfully registered. You may now log in."
        return False, "Failed to create account. Please try again."
    except Exception as e:
        return False, f"Registration failed due to a database error: {str(e)}"

def login_student_by_id(student_id: int) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Log in a student using verified student_id.
    Ensures biometric embeddings are stripped from session state.
    """
    student = get_student_by_id(student_id, include_embeddings=False)
    if not student:
        return False, "Student record not found.", None

    st.session_state.is_logged_in = True
    st.session_state.user_role = "student"
    st.session_state.student_data = student
    return True, f"Welcome back, {student.get('name')}!", student

def register_student(
    name: str,
    face_embedding: Optional[list] = None,
    voice_embedding: Optional[list] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Register a new student profile with facial and optional voice embeddings.
    """
    clean_name = (name or "").strip()
    if len(clean_name) < 2 or len(clean_name) > 60:
        return False, "Full name must be between 2 and 60 characters.", None

    if not face_embedding:
        return False, "A facial capture is required for student registration.", None

    try:
        records = db_create_student(clean_name, face_embedding, voice_embedding)
        if records and len(records) > 0:
            student = records[0]
            st.session_state.is_logged_in = True
            st.session_state.user_role = "student"
            st.session_state.student_data = student
            return True, f"Profile created! Welcome, {clean_name}.", student
        return False, "Unable to save student profile.", None
    except Exception as e:
        return False, f"Registration failed: {str(e)}", None

def logout():
    """
    Safely purge all authenticated session credentials and volatile attendance states.
    """
    keys_to_clear = [
        "is_logged_in",
        "user_role",
        "teacher_data",
        "student_data",
        "login_type",
        "teacher_login_type",
        "attendance_images",
        "voice_attendance_results",
        "active_attendance_session",
        "current_teacher_tab",
        "confirm_saving"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
