"""
Audio validation utilities for voice biometric enrollment and recognition.
"""

from typing import Tuple, Optional
import io
import soundfile as sf
from src.config.app_config import (
    MAX_AUDIO_SIZE_BYTES,
    MIN_AUDIO_DURATION_SECONDS,
    MAX_AUDIO_DURATION_SECONDS
)

def validate_audio_payload(audio_bytes: Optional[bytes]) -> Tuple[bool, str, Optional[float]]:
    """
    Validates audio byte payload size, format, and duration.
    Returns: (is_valid, error_message, duration_in_seconds)
    """
    if audio_bytes is None:
        return False, "No audio data received. Please record or upload an audio sample.", None

    size_bytes = len(audio_bytes)
    if size_bytes == 0:
        return False, "Audio recording is empty (0 bytes). Please try recording again.", None

    if size_bytes > MAX_AUDIO_SIZE_BYTES:
        max_mb = MAX_AUDIO_SIZE_BYTES / (1024 * 1024)
        return False, f"Audio file exceeds maximum allowed size ({max_mb:.0f} MB).", None

    try:
        # Check audio readability and duration using soundfile
        with io.BytesIO(audio_bytes) as bio:
            with sf.SoundFile(bio) as sfile:
                duration = len(sfile) / float(sfile.samplerate)
                
                if duration < MIN_AUDIO_DURATION_SECONDS:
                    return False, f"Audio sample is too short ({duration:.1f}s). Minimum {MIN_AUDIO_DURATION_SECONDS}s required.", duration

                if duration > MAX_AUDIO_DURATION_SECONDS:
                    return False, f"Audio recording exceeds maximum duration ({MAX_AUDIO_DURATION_SECONDS:.0f}s).", duration

                return True, "", duration
    except Exception as e:
        # Fallback error for corrupt or unsupported audio container
        return False, f"Could not decode audio format: {str(e)}", None
