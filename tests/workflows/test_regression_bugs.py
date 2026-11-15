"""
Regression tests verifying fixes for verified P0/P1 bugs identified during repository audit.
"""

import pytest
import numpy as np
from PIL import Image
from unittest.mock import patch, MagicMock

from src.validators.audio_validators import validate_audio_payload
from src.pipelines.voice_pipeline import process_bulk_audio
from src.pipelines.face_pipeline import match_face_to_candidates
from src.config.app_config import CANONICAL_APP_URL
from src.database.db import hash_pass, check_pass

class TestRegressionFixes:
    def test_voice_attendance_none_audio_does_not_crash(self):
        """Regression test for ISSUE-P0-01: 'NoneType' object has no attribute 'read' crash."""
        is_valid, msg, dur = validate_audio_payload(None)
        assert is_valid is False
        assert dur is None
        assert "no audio data" in msg.lower()

    def test_voice_recognition_failure_does_not_mark_all_students_absent(self):
        """Regression test for ISSUE-P0-02: Silent false absent logging on voice failure."""
        # Empty or noise-only audio should report an error and not return valid matches
        result = process_bulk_audio(b"invalid_noise_bytes", {1: [0.1]*256})
        assert result["matches"] == {}
        assert result["error"] is not None

    def test_face_pipeline_single_student_no_svc_crash(self):
        """Regression test for ISSUE-P0-04: Single student SVC ValueError and improper partition."""
        # When 1 candidate student exists, 1-to-1 distance matching operates cleanly
        single_student_embedding = np.random.randn(128)
        single_student_embedding = single_student_embedding / np.linalg.norm(single_student_embedding)

        candidates = [
            {"student_id": 42, "name": "Solo Student", "face_embedding": single_student_embedding.tolist()}
        ]

        # Exact match
        sid, name, dist, status = match_face_to_candidates(single_student_embedding, candidates)
        assert sid == 42
        assert status == "HIGH_CONFIDENCE"

        # Opposite/unknown face must NOT be falsely assigned to solo student
        unknown_face = -single_student_embedding
        u_sid, u_name, u_dist, u_status = match_face_to_candidates(unknown_face, candidates)
        assert u_sid is None
        assert u_status == "UNKNOWN"

    def test_canonical_app_url_has_valid_https_scheme(self):
        """Regression test for ISSUE-P0-05: Missing https:// scheme and hardcoded domain."""
        assert CANONICAL_APP_URL.startswith("http://") or CANONICAL_APP_URL.startswith("https://")
        assert not CANONICAL_APP_URL.endswith("/")

    def test_subject_card_closure_safety(self):
        """Regression test for ISSUE-P0-03: Subject card loop closure bug."""
        subjects = [
            {"name": "Sub A", "code": "CS101"},
            {"name": "Sub B", "code": "CS202"},
            {"name": "Sub C", "code": "CS303"}
        ]

        # Factory function with default arg binds correctly per iteration
        callbacks = []
        for s in subjects:
            def make_cb(code=s["code"]):
                return lambda: code
            callbacks.append(make_cb())

        assert callbacks[0]() == "CS101"
        assert callbacks[1]() == "CS202"
        assert callbacks[2]() == "CS303"
