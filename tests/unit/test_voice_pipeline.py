"""
Unit tests for voice recognition pipeline and speaker similarity scoring.
"""

import pytest
import numpy as np
from src.pipelines.voice_pipeline import (
    compute_cosine_similarity,
    identify_speaker,
    process_bulk_audio
)

class TestVoicePipeline:
    def test_cosine_similarity_properties(self):
        v1 = np.random.randn(256)
        v1 = v1 / np.linalg.norm(v1)

        # Self similarity = 1.0
        assert pytest.approx(compute_cosine_similarity(v1, v1), 1e-4) == 1.0

        # Opposite similarity = -1.0
        assert pytest.approx(compute_cosine_similarity(v1, -v1), 1e-4) == -1.0

        # Zero vector handled safely without division by zero
        zero_vec = np.zeros(256)
        assert compute_cosine_similarity(v1, zero_vec) == 0.0

    def test_identify_speaker_high_confidence(self):
        target = np.zeros(256)
        target[0] = 1.0

        candidates = {
            101: target.tolist(),
            102: np.zeros(256).tolist()
        }

        sid, score, status = identify_speaker(target, candidates, confidence_threshold=0.72)
        assert sid == 101
        assert score == 1.0
        assert status == "HIGH_CONFIDENCE"

    def test_identify_speaker_ambiguous_threshold(self):
        v1 = np.zeros(256)
        v1[0] = 1.0

        # Create candidate with ~0.65 similarity
        v2 = np.zeros(256)
        v2[0] = 0.65
        v2[1] = np.sqrt(1 - 0.65**2)

        candidates = {201: v2.tolist()}

        sid, score, status = identify_speaker(
            v1, candidates,
            confidence_threshold=0.72,
            ambiguous_threshold=0.58
        )
        assert sid == 201
        assert pytest.approx(score, 1e-2) == 0.65
        assert status == "NEEDS_REVIEW"

    def test_identify_speaker_unknown(self):
        v1 = np.zeros(256)
        v1[0] = 1.0

        v2 = np.zeros(256)
        v2[1] = 1.0  # orthogonal: score 0.0

        candidates = {301: v2.tolist()}

        sid, score, status = identify_speaker(v1, candidates)
        assert sid is None
        assert status == "UNKNOWN"

    def test_process_bulk_audio_empty_bytes(self):
        result = process_bulk_audio(b"", {1: [0.1]*256})
        assert result["matches"] == {}
        assert result["segments_processed"] == 0
        assert result["error"] is not None
        assert "empty" in result["error"].lower()

    def test_process_bulk_audio_none_bytes(self):
        result = process_bulk_audio(None, {1: [0.1]*256})
        assert result["matches"] == {}
        assert result["error"] is not None

    def test_identify_speaker_skips_invalid_embeddings(self):
        query = np.zeros(256)
        query[0] = 1.0

        candidates = {
            1: None,
            2: [0.1] * 10,  # invalid dimension (10 instead of 256)
            3: "not_a_vector"
        }
        sid, score, status = identify_speaker(query, candidates)
        assert sid is None
        assert status == "UNKNOWN"

    def test_identify_speaker_picks_best_match_among_candidates(self):
        query = np.zeros(256)
        query[0] = 1.0

        # c1 has cosine similarity 0.60 with query
        c1 = np.zeros(256)
        c1[0] = 0.60
        c1[1] = np.sqrt(1 - 0.60**2)

        # c2 has cosine similarity 0.95 with query
        c2 = np.zeros(256)
        c2[0] = 0.95
        c2[1] = np.sqrt(1 - 0.95**2)

        candidates = {101: c1.tolist(), 102: c2.tolist()}
        sid, score, status = identify_speaker(query, candidates)
        assert sid == 102
        assert status == "HIGH_CONFIDENCE"
        assert score > 0.90

    def test_similar_voice_speakers_downgraded_to_needs_review(self):
        query = np.zeros(256)
        query[0] = 1.0

        # Speaker 1 has similarity 0.96
        s1 = np.zeros(256)
        s1[0] = 0.96
        s1[1] = np.sqrt(1 - 0.96**2)

        # Speaker 2 has similarity 0.93 (gap is 0.03 < 0.05)
        s2 = np.zeros(256)
        s2[0] = 0.93
        s2[1] = np.sqrt(1 - 0.93**2)

        candidates = {201: s1.tolist(), 202: s2.tolist()}
        sid, score, status = identify_speaker(query, candidates)
        assert sid == 201
        assert status == "NEEDS_REVIEW"
