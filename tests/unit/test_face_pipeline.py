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

    def test_multiple_candidates_picks_closest(self, mock_candidates):
        # Create query very close to Bob (student 2)
        query = np.zeros(128)
        query[1] = 0.98
        query[3] = 0.1
        query = query / np.linalg.norm(query)

        sid, name, dist, status = match_face_to_candidates(query, mock_candidates)
        assert sid == 2
        assert name == "Bob Jones"
        assert status == "HIGH_CONFIDENCE"

    def test_scoped_candidate_isolation(self):
        # Candidate 5 is enrolled in Subject A, Candidate 9 is in Subject B
        v_subj_a = np.zeros(128)
        v_subj_a[5] = 1.0

        v_subj_b = np.zeros(128)
        v_subj_b[9] = 1.0

        # Roster for Subject A only
        roster_a = [{"student_id": 5, "name": "Student A", "face_embedding": v_subj_a.tolist()}]

        # Query of Student B against Subject A roster must be UNKNOWN
        sid, name, dist, status = match_face_to_candidates(v_subj_b, roster_a)
        assert sid is None
        assert status == "UNKNOWN"

    def test_similar_candidates_downgraded_to_needs_review(self):
        # Two very similar candidates (e.g. twins or duplicate enrollments)
        v1 = np.zeros(128)
        v1[0] = 1.0

        v2 = np.zeros(128)
        v2[0] = 0.999
        v2[1] = np.sqrt(1 - 0.999**2)

        candidates = [
            {"student_id": 1, "name": "Twin A", "face_embedding": v1.tolist()},
            {"student_id": 2, "name": "Twin B", "face_embedding": v2.tolist()}
        ]

        # Query identical to Twin A
        query = v1.copy()
        sid, name, dist, status = match_face_to_candidates(query, candidates)

        # Because distance to Twin A is 0.0 and distance to Twin B is ~0.045 (< 0.05),
        # system must downgrade to NEEDS_REVIEW to prevent false attribution
        assert sid == 1
        assert status == "NEEDS_REVIEW"
