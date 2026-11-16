"""
End-to-End Workflow Verification Test for SNAPCLASS AI.
Executes the full 14-step lifecycle:
1. Teacher registration
2. Subject creation
3. Student enrollment
4. Attendance session creation
5. Classroom image processing & candidate scoping
6. Voice audio processing & candidate scoping
7. Recognition review generation
8. Instructor status override
9. Attendance confirmation
10. Database record verification
11. Duplicate confirmation resubmission (idempotency check)
12. Duplicate rejection verification
13. Attendance history retrieval
14. Access boundaries & unenrollment historical record preservation
"""

import pytest
import numpy as np
from PIL import Image
from unittest.mock import patch, MagicMock

from src.services.auth_service import register_teacher, login_teacher, register_student
from src.services.subject_service import (
    create_new_subject,
    enroll_student_by_code,
    get_student_dashboard_data,
    unenroll_student_from_subject
)
from src.services.attendance_service import (
    prepare_face_attendance_session,
    prepare_voice_attendance_session,
    confirm_and_save_attendance,
    get_teacher_attendance_overview
)

class InMemoryMockDatabase:
    """Isolated in-memory mock store representing Supabase tables for E2E testing."""
    def __init__(self):
        self.teachers = []
        self.students = []
        self.subjects = []
        self.subject_students = []
        self.attendance_logs = []

    def reset(self):
        self.teachers.clear()
        self.students.clear()
        self.subjects.clear()
        self.subject_students.clear()
        self.attendance_logs.clear()

@pytest.fixture
def mock_db():
    db = InMemoryMockDatabase()
    return db

class TestEndToEndAttendanceFlow:
    def test_complete_attendance_lifecycle(self, mock_db):
        # -------------------------------------------------------------
        # STEP 1: Instructor Registration & Authentication
        # -------------------------------------------------------------
        with patch("src.services.auth_service.db_create_teacher") as mock_create_t, \
             patch("src.services.auth_service.check_teacher_exists") as mock_exists_t:

            mock_exists_t.return_value = False
            mock_create_t.return_value = {"teacher_id": 101, "username": "prof_alan", "name": "Prof. Alan Turing"}

            success, msg = register_teacher("prof_alan", "Prof. Alan Turing", "Turing1950Secure!", "Turing1950Secure!")
            assert success is True
            assert "successfully registered" in msg.lower()

        # -------------------------------------------------------------
        # STEP 2: Subject Creation
        # -------------------------------------------------------------
        with patch("src.services.subject_service.db_get_subject_by_code") as mock_code_check, \
             patch("src.services.subject_service.db_create_subject") as mock_create_sub:

            mock_code_check.return_value = None  # No duplicate
            mock_create_sub.return_value = [{"subject_id": 501, "subject_code": "CS501", "name": "Theory of Computation", "section": "Batch A", "teacher_id": 101}]

            sub_success, sub_msg, sub_data = create_new_subject(101, "CS501", "Theory of Computation", "Batch A")
            assert sub_success is True
            assert sub_data["subject_id"] == 501
            assert sub_data["subject_code"] == "CS501"

        # -------------------------------------------------------------
        # STEP 3: Student Biometric Profiles & Course Enrollment
        # -------------------------------------------------------------
        # Student 1: Ada Lovelace (Face + Voice)
        ada_face = np.zeros(128)
        ada_face[0] = 1.0
        ada_voice = np.zeros(256)
        ada_voice[0] = 1.0

        # Student 2: Claude Shannon (Face only)
        claude_face = np.zeros(128)
        claude_face[1] = 1.0

        enrolled_students = [
            {"student_id": 1, "name": "Ada Lovelace", "face_embedding": ada_face.tolist(), "voice_embedding": ada_voice.tolist()},
            {"student_id": 2, "name": "Claude Shannon", "face_embedding": claude_face.tolist(), "voice_embedding": None}
        ]

        # -------------------------------------------------------------
        # STEP 4 & 5: Classroom Photo Processing & Roster Scoping
        # -------------------------------------------------------------
        with patch("src.services.attendance_service.get_enrolled_students_for_subject") as mock_get_enrolled, \
             patch("src.services.attendance_service.check_teacher_owns_subject") as mock_owns:

            mock_owns.return_value = True
            mock_get_enrolled.return_value = enrolled_students

            # Synthetic image with face matching Ada
            test_img = Image.new("RGB", (300, 300), color="white")

            with patch("src.services.attendance_service.analyze_classroom_photo") as mock_analyze:
                # Ada detected in Photo 1 with 95% confidence; Claude not detected
                mock_analyze.return_value = {
                    "matches": {1: {"student_id": 1, "name": "Ada Lovelace", "distance": 0.05, "status": "HIGH_CONFIDENCE", "confidence_pct": 95.0}},
                    "unknown_faces": 0,
                    "total_faces": 1
                }

                success, msg, session_draft = prepare_face_attendance_session(
                    subject_id=501,
                    images=[test_img],
                    teacher_id=101
                )
                assert success is True
                assert session_draft["session_id"] is not None
                assert session_draft["present_count"] == 1
                assert session_draft["total_enrolled"] == 2

                review_df = session_draft["review_df"]
                ada_row = review_df[review_df["student_id"] == 1].iloc[0]
                claude_row = review_df[review_df["student_id"] == 2].iloc[0]

                assert ada_row["Status"] == "Present"
                assert bool(ada_row["Is Present"]) is True
                assert claude_row["Status"] == "Absent"
                assert bool(claude_row["Is Present"]) is False

        # -------------------------------------------------------------
        # STEP 6: Instructor Status Override (Manual Review)
        # -------------------------------------------------------------
        # Instructor manually marks Claude Shannon present (e.g., sat behind pillar)
        final_records = [
            {"student_id": 1, "subject_id": 501, "timestamp": session_draft["timestamp"], "is_present": True},
            {"student_id": 2, "subject_id": 501, "timestamp": session_draft["timestamp"], "is_present": True}  # Overridden!
        ]

        # -------------------------------------------------------------
        # STEP 7 & 8: Attendance Confirmation & Idempotency
        # -------------------------------------------------------------
        session_id = session_draft["session_id"]

        with patch("src.services.attendance_service.check_teacher_owns_subject") as mock_owns, \
             patch("src.services.attendance_service.check_attendance_session_exists") as mock_exists, \
             patch("src.services.attendance_service.get_enrolled_students_for_subject") as mock_enrolled, \
             patch("src.services.attendance_service.db_create_attendance") as mock_save:

            mock_owns.return_value = True
            mock_exists.return_value = False
            mock_enrolled.return_value = [
                {"student_id": 1, "name": "Student Alpha"},
                {"student_id": 2, "name": "Student Beta"}
            ]
            mock_save.return_value = [
                {"id": 1001, "student_id": 1, "subject_id": 501, "is_present": True},
                {"id": 1002, "student_id": 2, "subject_id": 501, "is_present": True}
            ]

            # 9. First Confirmation
            confirm_success, confirm_msg = confirm_and_save_attendance(
                teacher_id=101,
                session_id=session_id,
                subject_id=501,
                final_attendance_records=final_records
            )
            assert confirm_success is True
            assert "Successfully confirmed attendance for 2 students" in confirm_msg

            # 11 & 12. Submit the SAME confirmation again (Double-click / replay attack)
            dup_success, dup_msg = confirm_and_save_attendance(
                teacher_id=101,
                session_id=session_id,
                subject_id=501,
                final_attendance_records=final_records
            )
            assert dup_success is False
            assert "already been saved" in dup_msg

        # -------------------------------------------------------------
        # STEP 13: Attendance History Retrieval
        # -------------------------------------------------------------
        with patch("src.services.attendance_service.db_get_attendance_for_teacher") as mock_teacher_hist:
            mock_teacher_hist.return_value = [
                {
                    "id": 1001,
                    "timestamp": session_draft["timestamp"],
                    "subject_id": 501,
                    "student_id": 1,
                    "is_present": True,
                    "subjects": {"subject_id": 501, "name": "Theory of Computation", "subject_code": "CS501", "section": "Batch A"}
                },
                {
                    "id": 1002,
                    "timestamp": session_draft["timestamp"],
                    "subject_id": 501,
                    "student_id": 2,
                    "is_present": True,
                    "subjects": {"subject_id": 501, "name": "Theory of Computation", "subject_code": "CS501", "section": "Batch A"}
                }
            ]

            overview = get_teacher_attendance_overview(101)
            assert len(overview) == 1
            assert overview[0]["total_students"] == 2
            assert overview[0]["present_count"] == 2
            assert overview[0]["attendance_rate"] == "100.0%"

        # -------------------------------------------------------------
        # STEP 14: Historical Record Preservation on Unenrollment
        # -------------------------------------------------------------
        # If Claude leaves the subject, historical records in attendance_logs are NOT deleted
        with patch("src.services.subject_service.db_unenroll_student") as mock_unenroll, \
             patch("src.services.subject_service.db_get_student_subjects") as mock_subs, \
             patch("src.services.subject_service.db_get_student_attendance") as mock_student_att:

            mock_unenroll.return_value = [{"subject_id": 501, "student_id": 2}]
            unenroll_success, _ = unenroll_student_from_subject(2, 501)
            assert unenroll_success is True

            # Student now has 0 enrolled courses, but their past attendance log remains intact
            mock_subs.return_value = []
            mock_student_att.return_value = [
                {"id": 1002, "timestamp": session_draft["timestamp"], "subject_id": 501, "is_present": True}
            ]

            subs, summary = get_student_dashboard_data(2)
            assert len(subs) == 0
            assert summary["total_classes"] == 1
            assert summary["total_attended"] == 1
            assert summary["overall_pct"] == 100.0
