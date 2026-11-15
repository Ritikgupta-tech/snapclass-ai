"""
Unit tests for facial recognition pipeline and candidate matching.
"""

import pytest
import numpy as np
from src.pipelines.face_pipeline import (
    match_face_to_candidates,
    analyze_classroom_photo
)

class TestFacePipeline:
    @pytest.fixture
    def mock_candidates(self):
        # 128-d unit vectors
        v1 = np.zeros(128)
        v1[0] = 1.0  # student 1

        v2 = np.zeros(128)
        v2[1] = 1.0  # student 2

        return [
            {"student_id": 1, "name": "Alice Smith", "face_embedding": v1.tolist()},
            {"student_id": 2, "name": "Bob Jones", "face_embedding": v2.tolist()},
        ]

    def test_exact_face_match(self, mock_candidates):
        # Target identical to Alice
        query = np.zeros(128)
        query[0] = 1.0

        sid, name, dist, status = match_face_to_candidates(query, mock_candidates)
        assert sid == 1
        assert name == "Alice Smith"
        assert dist < 0.001
        assert status == "HIGH_CONFIDENCE"

    def test_ambiguous_face_match(self, mock_candidates):
        # Target with distance around 0.58
        query = np.zeros(128)
        query[0] = 0.83
        query[2] = 0.55  # normalized approximately 1.0
        query = query / np.linalg.norm(query)

        sid, name, dist, status = match_face_to_candidates(
            query, mock_candidates,
            distance_threshold=0.55,
            ambiguous_threshold=0.65
        )
        assert sid == 1
        assert status == "NEEDS_REVIEW"

    def test_unknown_face(self, mock_candidates):
        # Target orthogonal to both candidates
        query = np.zeros(128)
        query[10] = 1.0

        sid, name, dist, status = match_face_to_candidates(query, mock_candidates)
        assert sid is None
        assert status == "UNKNOWN"

    def test_empty_candidates_returns_unknown(self):
        query = np.ones(128) / np.sqrt(128)
        sid, name, dist, status = match_face_to_candidates(query, [])
        assert sid is None
        assert status == "UNKNOWN"

    def test_corrupt_candidate_vector_handled_gracefully(self):
        bad_candidates = [
            {"student_id": 99, "name": "Bad Data", "face_embedding": [0.1, 0.2]},  # wrong length!
            {"student_id": 100, "name": "None Data", "face_embedding": None}
        ]
        query = np.ones(128) / np.sqrt(128)
        sid, name, dist, status = match_face_to_candidates(query, bad_candidates)
        assert sid is None
        assert status == "UNKNOWN"
