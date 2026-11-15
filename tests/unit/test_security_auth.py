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

    def test_rate_limiting_persists_across_streamlit_session_restarts(self):
        username = "persistent_attacker"
        _clear_failed_attempts(username)

        # Trigger lockout
        for _ in range(5):
            _record_failed_attempt(username)

        assert _is_rate_limited(username)[0] is True

        # Simulate clearing st.session_state (session restart or new incognito tab)
        st.session_state.clear()

        # Cooldown MUST still be enforced process-wide
        is_limited, remaining = _is_rate_limited(username)
        assert is_limited is True
        assert remaining > 0

        _clear_failed_attempts(username)

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
        st.session_state["_cached_teacher_subjects"] = [{"subject_id": 1}]
        st.session_state["_cached_student_dashboard"] = ([], {})

        logout()

        assert "is_logged_in" not in st.session_state
        assert "user_role" not in st.session_state
        assert "teacher_data" not in st.session_state
        assert "attendance_images" not in st.session_state
        assert "_cached_teacher_subjects" not in st.session_state
        assert "_cached_student_dashboard" not in st.session_state

    def test_rate_limiting_composite_ip_spraying_lockout(self):
        attacker_ip = "198.51.100.42"
        _clear_failed_attempts("any_user", attacker_ip)

        # Attacker tries different usernames from same IP (15 attempts triggers IP lockout: 3 * MAX_LOGIN_ATTEMPTS)
        for i in range(15):
            u = f"target_user_{i}"
            _record_failed_attempt(u, attacker_ip)

        # A brand new username from this attacker IP must now be locked out
        limited, remaining = _is_rate_limited("brand_new_user", attacker_ip)
        assert limited is True
        assert remaining > 0

        # Clean up
        _clear_failed_attempts("brand_new_user", attacker_ip)

    def test_missing_credentials_handled_gracefully(self):
        # Empty or whitespace usernames
        success, msg, data = login_teacher("", "")
        assert success is False
        assert "required" in msg.lower()

        success, msg, data = login_teacher("   ", "password")
        assert success is False
        assert "required" in msg.lower()

    def test_cross_subject_unauthorized_teacher_injection(self):
        from src.services.attendance_service import confirm_and_save_attendance
        with patch("src.services.attendance_service.check_teacher_owns_subject") as mock_owns:
            mock_owns.return_value = False
            success, msg = confirm_and_save_attendance(
                teacher_id=999,  # attacker teacher ID
                session_id="unauth_sess_1",
                subject_id=42,    # victim's subject
                final_attendance_records=[{"student_id": 1, "is_present": True}]
            )
            assert success is False
            assert "unauthorized" in msg.lower()

    def test_teacher_cannot_access_other_teacher_subjects(self):
        """Verify Teacher A cannot query or own subjects created by Teacher B."""
        from src.database.db import check_teacher_owns_subject

        with patch("src.database.db.supabase") as mock_sp:
            def mock_table(table_name):
                class MockQuery:
                    def __init__(self):
                        self.filters = {}
                    def select(self, *args, **kwargs):
                        return self
                    def eq(self, col, val):
                        self.filters[col] = val
                        return self
                    def execute(self):
                        # Subject 99 belongs to teacher_id 20
                        if self.filters.get("subject_id") == 99 and self.filters.get("teacher_id") == 20:
                            return MagicMock(data=[{"subject_id": 99, "teacher_id": 20}])
                        return MagicMock(data=[])
                return MockQuery()

            mock_sp.table.side_effect = mock_table

            # Teacher A (ID 10) attempts to access subject 99 owned by Teacher B (ID 20)
            is_owner = check_teacher_owns_subject(teacher_id=10, subject_id=99)
            assert is_owner is False

            # Teacher B (ID 20) attempts to access subject 99
            is_owner_b = check_teacher_owns_subject(teacher_id=20, subject_id=99)
            assert is_owner_b is True

    def test_teacher_cannot_access_other_teacher_attendance_records(self):
        """Verify attendance overview query filters strictly by teacher_id at the DB layer."""
        from src.database.db import get_attendance_for_teacher

        with patch("src.database.db.supabase") as mock_sp:
            mock_table = MagicMock()
            mock_sp.table.return_value = mock_table
            mock_table.select.return_value = mock_table
            mock_table.eq.return_value = mock_table
            mock_table.order.return_value = mock_table
            mock_table.execute.return_value = MagicMock(data=[])

            get_attendance_for_teacher(teacher_id=101)

            # Assert .eq("subjects.teacher_id", 101) was strictly invoked
            mock_table.eq.assert_called_with("subjects.teacher_id", 101)

    def test_students_cannot_submit_attendance_for_other_students(self):
        """Verify unauthenticated student/attacker cannot invoke confirm_and_save_attendance."""
        from src.services.attendance_service import confirm_and_save_attendance

        # Student ID passed as teacher_id
        with patch("src.services.attendance_service.check_teacher_owns_subject") as mock_owns:
            mock_owns.return_value = False
            success, msg = confirm_and_save_attendance(
                teacher_id=None,  # student has no teacher_id
                session_id="student_exploit_session",
                subject_id=1,
                final_attendance_records=[{"student_id": 999, "is_present": True}]
            )
            assert success is False
            assert "unauthorized" in msg.lower()

    def test_raw_embeddings_and_passwords_never_exposed_in_session_state(self):
        """Verify raw 128-d / 256-d vectors and password hashes are stripped before state population."""
        from src.services.auth_service import login_student_by_id, register_student
        from src.database.db import teacher_login, create_student

        # 1. Teacher login strips password
        with patch("src.database.db.supabase") as mock_sp:
            mock_sp.table.return_value.select.return_value.eq.return_value.execute.return_value = MagicMock(
                data=[{
                    "teacher_id": 1,
                    "username": "prof_secure",
                    "password": hash_pass("ValidPass123"),
                    "name": "Prof Secure"
                }]
            )
            teacher = teacher_login("prof_secure", "ValidPass123")
            assert teacher is not None
            assert "password" not in teacher
            assert "password_hash" not in teacher

        # 2. Student login excludes embeddings
        with patch("src.services.auth_service.get_student_by_id") as mock_get_st:
            mock_get_st.return_value = {"student_id": 50, "name": "Safe Student"}
            st.session_state.clear()
            success, msg, student = login_student_by_id(50)
            assert success is True
            assert "face_embedding" not in st.session_state.student_data
            assert "voice_embedding" not in st.session_state.student_data
            mock_get_st.assert_called_with(50, include_embeddings=False)

    def test_invalid_or_expired_authentication_rejected(self):
        """Verify invalid passwords or non-existent student IDs return clean rejection."""
        from src.services.auth_service import login_student_by_id

        # 1. Non-existent student
        with patch("src.services.auth_service.get_student_by_id") as mock_get:
            mock_get.return_value = None
            success, msg, data = login_student_by_id(999999)
            assert success is False
            assert "not found" in msg.lower()
            assert data is None

        # 2. Invalid teacher password
        with patch("src.services.auth_service.db_teacher_login") as mock_login:
            mock_login.return_value = None
            success, msg, data = login_teacher("valid_user", "WrongPassword123")
            assert success is False
            assert "invalid" in msg.lower()
            assert data is None
