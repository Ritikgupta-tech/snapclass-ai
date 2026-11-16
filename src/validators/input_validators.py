"""
Input validation utilities for user registration, authentication, and subject management.
"""

import re
from typing import Tuple
from src.config.app_config import MIN_PASSWORD_LENGTH

def validate_username(username: str) -> Tuple[bool, str]:
    """Validate username format (alphanumeric, underscores, 3-30 chars)."""
    if not username:
        return False, "Username is required."
    clean = username.strip()
    if len(clean) < 3 or len(clean) > 30:
        return False, "Username must be between 3 and 30 characters."
    if not re.match(r"^[a-zA-Z0-9_.-]+$", clean):
        return False, "Username may only contain letters, numbers, periods, dashes, and underscores."
    return True, ""

def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength (length and basic complexity)."""
    if not password:
        return False, "Password is required."
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    return True, ""

def validate_subject_inputs(subject_code: str, name: str, section: str) -> Tuple[bool, str]:
    """Validate inputs for subject creation."""
    code = (subject_code or "").strip()
    s_name = (name or "").strip()
    sec = (section or "").strip()

    if not code:
        return False, "Subject code is required (e.g. CS101)."
    if len(code) < 2 or len(code) > 20:
        return False, "Subject code must be between 2 and 20 characters."
    if not re.match(r"^[a-zA-Z0-9_-]+$", code):
        return False, "Subject code can only contain alphanumeric characters, hyphens, and underscores."
    
    if not s_name:
        return False, "Subject name is required."
    if len(s_name) < 2 or len(s_name) > 100:
        return False, "Subject name must be between 2 and 100 characters."

    if not sec:
        return False, "Section is required (e.g. Section A, Batch 2026)."
    if len(sec) > 30:
        return False, "Section cannot exceed 30 characters."

    return True, ""

def sanitize_string(val: str, max_length: int = 255) -> str:
    """Strip whitespace and enforce length boundary."""
    if not val:
        return ""
    return str(val).strip()[:max_length]
