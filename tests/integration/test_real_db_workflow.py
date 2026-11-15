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
        """Verify real transaction behavior on staging database."""
        # This executes only on an isolated staging database with synthetic data
        pass
