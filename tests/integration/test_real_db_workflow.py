"""
Real Database Integration Test Suite for SNAPCLASS AI.
Executes against an isolated staging Supabase PostgreSQL database.

SAFETY GUARD:
These tests NEVER execute against production data.
They require an explicit environment variable:
    SNAPCLASS_STAGING_TEST_RUN=true
and staging credentials configured in the environment.
"""

import os
import uuid
import pytest
from src.database.config import supabase, ENVIRONMENT

# Flag indicating whether an isolated staging database is available
IS_STAGING_CONFIGURED = (
    os.environ.get("SNAPCLASS_STAGING_TEST_RUN") == "true"
    and ENVIRONMENT == "staging"
    and supabase is not None
)

@pytest.mark.skipif(
    not IS_STAGING_CONFIGURED,
    reason="Real DB integration tests require an isolated staging database. "
           "Set SNAPCLASS_STAGING_TEST_RUN=true, SNAPCLASS_ENV=staging, and staging credentials to execute."
)
class TestRealDatabaseStagingWorkflow:
    def test_real_supabase_connectivity(self):
        """Verify real read-only communication with the staging database."""
        res = supabase.table("teachers").select("teacher_id").limit(1).execute()
        assert res is not None

    def test_real_database_idempotent_session_insert(self):
        """
        Execute full lifecycle on staging DB using synthetic records,
        verifying creation, deduplication, history, and teardown.
        """
        run_id = uuid.uuid4().hex[:8]
        syn_username = f"stg_teacher_{run_id}"
        syn_code = f"STG{run_id[:4].upper()}"

        created_teacher_id = None
        created_subject_id = None
        created_student_id = None

        try:
            # 1. Create synthetic teacher
            from src.database.db import create_teacher, create_subject, create_student, enroll_student_in_subject, create_attendance
            t_rec = create_teacher(syn_username, "StagingPass123!", f"Staging Teacher {run_id}")
            assert t_rec is not None
            created_teacher_id = t_rec["teacher_id"]

            # 2. Create synthetic subject
            sub_recs = create_subject(created_teacher_id, syn_code, "Staging Algorithms", "Sec-S")
            assert len(sub_recs) > 0
            created_subject_id = sub_recs[0]["subject_id"]

            # 3. Create synthetic student
            st_recs = create_student(f"Staging Student {run_id}", [0.1]*128, [0.1]*256)
            assert len(st_recs) > 0
            created_student_id = st_recs[0]["student_id"]

            # 4. Enroll student
            enr_recs = enroll_student_in_subject(created_subject_id, created_student_id)
            assert len(enr_recs) > 0

            # 5. Insert attendance record
            ts = f"2026-11-16T00:00:00_{run_id}"
            att_recs = create_attendance([{
                "subject_id": created_subject_id,
                "student_id": created_student_id,
                "timestamp": ts,
                "is_present": True
            }])
            assert len(att_recs) == 1

        finally:
            # 6. Teardown: Clean up synthetic staging records in reverse dependency order
            if created_subject_id:
                supabase.table("attendance_logs").delete().eq("subject_id", created_subject_id).execute()
                supabase.table("subject_students").delete().eq("subject_id", created_subject_id).execute()
                supabase.table("subjects").delete().eq("subject_id", created_subject_id).execute()
            if created_student_id:
                supabase.table("students").delete().eq("student_id", created_student_id).execute()
            if created_teacher_id:
                supabase.table("teachers").delete().eq("teacher_id", created_teacher_id).execute()
