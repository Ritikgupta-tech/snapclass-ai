"""
Voice recognition pipeline for SNAPCLASS AI.
Uses Resemblyzer deep speaker embeddings and cosine similarity scoring.
"""

from typing import Dict, Tuple, Optional, Any, List
import io
import logging
import numpy as np
import librosa
from resemblyzer import VoiceEncoder, preprocess_wav
import streamlit as st

from src.config.app_config import (
    VOICE_CONFIDENCE_THRESHOLD,
    VOICE_AMBIGUOUS_THRESHOLD,
    VOICE_SAMPLE_RATE,
    MIN_AUDIO_DURATION_SECONDS
)
from src.validators.audio_validators import validate_audio_payload

logger = logging.getLogger(__name__)

@st.cache_resource
def load_voice_encoder() -> VoiceEncoder:
    """
    Load pre-trained Resemblyzer voice encoder model.
    Cached at process level to avoid disk re-reads.
    """
    return VoiceEncoder()

def get_voice_embedding(audio_bytes: bytes) -> Optional[List[float]]:
    """
    Extract 256-dimensional speaker embedding from raw audio bytes.
    Returns normalized float list or None on error.
    """
    is_valid, err_msg, duration = validate_audio_payload(audio_bytes)
    if not is_valid:
        logger.warning(f"Audio payload validation failed: {err_msg}")
        return None

    try:
        encoder = load_voice_encoder()
        with io.BytesIO(audio_bytes) as bio:
            audio, sr = librosa.load(bio, sr=VOICE_SAMPLE_RATE)
        
        wav = preprocess_wav(audio)
        if len(wav) < VOICE_SAMPLE_RATE * MIN_AUDIO_DURATION_SECONDS:
            logger.warning("Preprocessed audio utterance is too brief.")
            return None

        raw_embedding = encoder.embed_utterance(wav)
        norm = np.linalg.norm(raw_embedding)
        if norm > 0:
            normed_embedding = raw_embedding / norm
        else:
            normed_embedding = raw_embedding

        return normed_embedding.tolist()
    except Exception as e:
        logger.error(f"Failed to generate voice embedding: {e}")
        return None

def compute_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Calculate normalized cosine similarity between two vectors."""
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

def identify_speaker(
    segment_embedding: np.ndarray,
    candidates_dict: Dict[int, Any],
    confidence_threshold: float = VOICE_CONFIDENCE_THRESHOLD,
    ambiguous_threshold: float = VOICE_AMBIGUOUS_THRESHOLD
) -> Tuple[Optional[int], float, str]:
    """
    Compare a speech segment embedding against enrolled candidate embeddings.
    Returns: (best_student_id, best_score, status)
    where status is 'HIGH_CONFIDENCE', 'NEEDS_REVIEW', or 'UNKNOWN'.
    """
    if segment_embedding is None or not candidates_dict:
        return None, 0.0, "UNKNOWN"

    best_sid = None
    best_score = -1.0
    second_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if not stored_embedding:
            continue
        try:
            cand_vec = np.array(stored_embedding, dtype=np.float64)
            if cand_vec.shape[0] != 256:
                continue
            sim = compute_cosine_similarity(segment_embedding, cand_vec)
            if sim > best_score:
                second_score = best_score
                best_score = sim
                best_sid = sid
            elif sim > second_score:
                second_score = sim
        except Exception as e:
            logger.warning(f"Error computing similarity for candidate {sid}: {e}")
            continue

    # If top candidate and runner-up candidate have very close scores (gap < 0.05),
    # downgrade to NEEDS_REVIEW to prevent false speaker attribution
    if (best_score - second_score) < 0.05 and best_score >= confidence_threshold:
        return best_sid, round(best_score, 4), "NEEDS_REVIEW"

    if best_score >= confidence_threshold:
        return best_sid, round(best_score, 4), "HIGH_CONFIDENCE"
    elif best_score >= ambiguous_threshold:
        return best_sid, round(best_score, 4), "NEEDS_REVIEW"
    else:
        return None, round(max(0.0, best_score), 4), "UNKNOWN"

def process_bulk_audio(
    audio_bytes: bytes,
    candidates_dict: Dict[int, Any],
    threshold: float = VOICE_CONFIDENCE_THRESHOLD
) -> Dict[str, Any]:
    """
    Process classroom audio recording, split on non-silent utterances,
    and match each utterance against enrolled candidate speaker embeddings.

    Returns dict with:
      - 'matches': dict[student_id -> {'score': float, 'status': str}]
      - 'segments_processed': int
      - 'error': Optional[str]
    """
    is_valid, err_msg, duration = validate_audio_payload(audio_bytes)
    if not is_valid:
        return {"matches": {}, "segments_processed": 0, "error": err_msg}

    try:
        encoder = load_voice_encoder()
        with io.BytesIO(audio_bytes) as bio:
            audio, sr = librosa.load(bio, sr=VOICE_SAMPLE_RATE)

        # Split speech on non-silent intervals
        segments = librosa.effects.split(audio, top_db=25)
        if len(segments) == 0:
            return {"matches": {}, "segments_processed": 0, "error": "No audible speech detected in recording."}

        identified_results: Dict[int, Dict[str, Any]] = {}
        processed_count = 0

        for start, end in segments:
            # Skip noise blips shorter than 0.4 seconds
            if (end - start) < sr * 0.4:
                continue

            processed_count += 1
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            segment_embedding = encoder.embed_utterance(wav)

            sid, score, status = identify_speaker(
                segment_embedding,
                candidates_dict,
                confidence_threshold=threshold,
                ambiguous_threshold=VOICE_AMBIGUOUS_THRESHOLD
            )

            if sid is not None and status in ("HIGH_CONFIDENCE", "NEEDS_REVIEW"):
                if sid not in identified_results or score > identified_results[sid]["score"]:
                    identified_results[sid] = {
                        "score": score,
                        "status": status,
                        "confidence_pct": round(score * 100, 1)
                    }

        return {
            "matches": identified_results,
            "segments_processed": processed_count,
            "error": None
        }

    except Exception as e:
        logger.error(f"Classroom audio processing failure: {e}", exc_info=True)
        return {
            "matches": {},
            "segments_processed": 0,
            "error": f"Audio processing error: {str(e)}"
        }
