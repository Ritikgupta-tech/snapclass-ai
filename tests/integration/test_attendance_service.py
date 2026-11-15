"""
Integration tests for attendance service and idempotent session confirmation.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.services.attendance_service import (
    confirm_and_save_attendance,
    get_teacher_attendance_overview
)

class TestAttendanceService:
    @patch("src.services.attendance_service.check_attendance_session_exists")
    @patch("src.services.attendance_service.check_teacher_owns_subject")
    @patch("src.services.attendance_service.db_create_attendance")
    def test_idempotent_confirmation(self, mock_create, mock_owns, mock_exists):
        mock_exists.return_value = False
        mock_owns.return_value = True
        mock_create.return_value = [{"id": 1, "student_id": 10, "is_present": True}]

        session_id = "test_sess_unique_123"
        records = [{"student_id": 10, "subject_id": 5, "timestamp": "2026-11-15T10:00:00", "is_present": True}]

        # First save: should succeed
        success, msg = confirm_and_save_attendance(teacher_id=1, session_id=session_id, subject_id=5, final_attendance_records=records)
        assert success is True
        assert "Successfully confirmed" in msg

        # Duplicate save with same session_id: must be rejected idempotently
        dup_success, dup_msg = confirm_and_save_attendance(teacher_id=1, session_id=session_id, subject_id=5, final_attendance_records=records)
        assert dup_success is False
        assert "already been saved" in dup_msg

    @patch("src.services.attendance_service.check_attendance_session_exists")
    @patch("src.services.attendance_service.check_teacher_owns_subject")
    def test_db_level_duplicate_timestamp_rejected(self, mock_owns, mock_exists):
        mock_owns.return_value = True
        mock_exists.return_value = True  # session already in DB!

        session_id = "new_sess_after_restart"
        records = [{"student_id": 10, "subject_id": 5, "timestamp": "2026-11-15T10:00:00", "is_present": True}]

        success, msg = confirm_and_save_attendance(teacher_id=1, session_id=session_id, subject_id=5, final_attendance_records=records)
        assert success is False
        assert "already been recorded in the database" in msg

    @patch("src.services.attendance_service.check_teacher_owns_subject")
    def test_unauthorized_teacher_rejected(self, mock_owns):
        mock_owns.return_value = False
        success, msg = confirm_and_save_attendance(
            teacher_id=99,
            session_id="unauth_sess",
            subject_id=5,
            final_attendance_records=[{"student_id": 1, "is_present": True}]
        )
        assert success is False
        assert "Unauthorized" in msg

    @patch("src.services.attendance_service.db_get_attendance_for_teacher")
    def test_get_teacher_attendance_overview_grouping(self, mock_get_att):
        mock_get_att.return_value = [
            {
                "id": 1,
                "timestamp": "2026-11-15T09:00:00",
                "subject_id": 1,
                "student_id": 101,
                "is_present": True,
                "subjects": {"name": "Data Structures", "subject_code": "CS201", "section": "A"}
            },
            {
                "id": 2,
                "timestamp": "2026-11-15T09:00:00",
                "subject_id": 1,
                "student_id": 102,
                "is_present": False,
                "subjects": {"name": "Data Structures", "subject_code": "CS201", "section": "A"}
            }
        ]

        overview = get_teacher_attendance_overview(1)
        assert len(overview) == 1
        sess = overview[0]
        assert sess["subject_name"] == "Data Structures"
        assert sess["total_students"] == 2
        assert sess["present_count"] == 1
        assert sess["attendance_rate"] == "50.0%"
