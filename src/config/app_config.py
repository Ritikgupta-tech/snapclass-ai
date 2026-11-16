"""
Centralized Application Configuration for SNAPCLASS AI.
Provides constants, recognition thresholds, and environment-driven defaults.
"""

import os
import streamlit as st

# Application URLs
DEFAULT_LIVE_URL = "https://snapclass-ai-attendence-system.streamlit.app"
try:
    CANONICAL_APP_URL = st.secrets.get("APP_URL", DEFAULT_LIVE_URL)
except Exception:
    CANONICAL_APP_URL = os.getenv("APP_URL", DEFAULT_LIVE_URL)

# Ensure URL has proper scheme and no trailing slash
if not CANONICAL_APP_URL.startswith("http://") and not CANONICAL_APP_URL.startswith("https://"):
    CANONICAL_APP_URL = f"https://{CANONICAL_APP_URL}"
CANONICAL_APP_URL = CANONICAL_APP_URL.rstrip("/")

# Audio & Voice Recognition Constraints
MAX_AUDIO_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit
MIN_AUDIO_DURATION_SECONDS = 0.5         # Minimum speech segment
MAX_AUDIO_DURATION_SECONDS = 60.0        # Max audio duration to prevent timeouts
VOICE_SAMPLE_RATE = 16000                # Resemblyzer standard sample rate
VOICE_CONFIDENCE_THRESHOLD = 0.72        # Cosine similarity for confident match
VOICE_AMBIGUOUS_THRESHOLD = 0.58         # Marginal match range (0.58 <= score < 0.72)

# Face Recognition Constraints
FACE_DISTANCE_THRESHOLD = 0.55           # dlib Euclidean distance for high-confidence match
FACE_AMBIGUOUS_THRESHOLD = 0.65          # 0.55 < d <= 0.65 requires teacher review
MAX_IMAGE_DIMENSION = 1920               # Max width/height to avoid memory spikes
FACE_DETECTION_UPSAMPLE = 1              # Standard dlib pyramid upsample

# Security & Authentication Constraints
MIN_PASSWORD_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 300           # 5 minutes
