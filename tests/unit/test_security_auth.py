"""
Unit tests for security, credential hashing, rate limiting, and sensitive field stripping.
"""

import pytest
import streamlit as st
from unittest.mock import patch, MagicMock

from src.database.db import hash_pass, check_pass
from src.services.auth_service import (
    _record_failed_attempt,
    _is_rate_limited,
    _clear_failed_attempts,
    login_teacher,
    register_teacher,
    logout
)

class TestSecurityAndAuth:
    def test_bcrypt_hashing_and_verification(self):
        pwd = "TestPassword123"
        hashed = hash_pass(pwd)
        assert hashed != pwd
        assert check_pass(pwd, hashed) is True
        assert check_pass("WrongPass", hashed) is False

    def test_rate_limiting_lockout_after_max_attempts(self):
        # Initialize test session state
        st.session_state["login_attempts_tracker"] = {}
        username = "brute_force_user"

        for _ in range(4):
            _record_failed_attempt(username)
            limited, _ = _is_rate_limited(username)
            assert limited is False

        # 5th failed attempt triggers lockout
        _record_failed_attempt(username)
        limited, remaining = _is_rate_limited(username)
        assert limited is True
        assert remaining > 0

        # Clearing attempts resets lockout
        _clear_failed_attempts(username)
        limited, _ = _is_rate_limited(username)
        assert limited is False

    def test_register_teacher_rejects_weak_passwords(self):
        success, msg = register_teacher("valid_user", "Teacher Name", "weak", "weak")
        assert success is False
        assert "at least 8" in msg

    def test_register_teacher_rejects_mismatched_passwords(self):
        success, msg = register_teacher("valid_user", "Teacher Name", "ValidPass123", "MismatchPass123")
        assert success is False
        assert "not match" in msg

    def test_logout_purges_authenticated_state(self):
        st.session_state["is_logged_in"] = True
        st.session_state["user_role"] = "teacher"
        st.session_state["teacher_data"] = {"teacher_id": 1, "username": "admin"}
        st.session_state["attendance_images"] = ["dummy_image"]

        logout()

        assert "is_logged_in" not in st.session_state
        assert "user_role" not in st.session_state
        assert "teacher_data" not in st.session_state
        assert "attendance_images" not in st.session_state
