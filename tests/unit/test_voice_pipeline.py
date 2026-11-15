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
