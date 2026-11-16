"""
Integration tests for subject service, enrollment logic, and QR generation.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.services.subject_service import (
    create_new_subject,
    enroll_student_by_code,
    generate_qr_share_details,
    get_student_dashboard_data
)
from src.config.app_config import CANONICAL_APP_URL

class TestSubjectService:
    def test_generate_qr_share_details(self):
        details = generate_qr_share_details("Machine Learning", "CS401")
        assert details["subject_code"] == "CS401"
        assert details["join_url"].startswith("http")
        assert f"join-code=CS401" in details["join_url"]
        assert len(details["qr_png_bytes"]) > 100

    @patch("src.services.subject_service.db_get_subject_by_code")
    def test_create_new_subject_duplicate_code_rejected(self, mock_get_code):
        mock_get_code.return_value = {"subject_id": 99, "subject_code": "CS101"}
        success, msg, data = create_new_subject(1, "CS101", "Computer Science", "Sec A")
        assert success is False
        assert "already taken" in msg
        assert data is None

    @patch("src.services.subject_service.db_get_student_subjects")
    @patch("src.services.subject_service.db_get_student_attendance")
    def test_get_student_dashboard_data_aggregations(self, mock_get_att, mock_get_subs):
        mock_get_subs.return_value = [
            {"subjects": {"subject_id": 1, "subject_code": "CS101", "name": "Algorithms", "section": "A"}}
        ]
        mock_get_att.return_value = [
            {"subject_id": 1, "is_present": True},
            {"subject_id": 1, "is_present": False},
            {"subject_id": 1, "is_present": True},
            {"subject_id": 1, "is_present": True}
        ]

        subjects, summary = get_student_dashboard_data(10)
        assert len(subjects) == 1
        assert subjects[0]["total_classes"] == 4
        assert subjects[0]["attended_classes"] == 3
        assert subjects[0]["attendance_pct"] == 75.0
        assert summary["total_classes"] == 4
        assert summary["total_attended"] == 3
        assert summary["overall_pct"] == 75.0
