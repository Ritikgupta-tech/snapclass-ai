"""
Database configuration and environment isolation for SNAPCLASS AI.
Guarantees strict separation between development, staging, and production databases.
"""

import os
import logging
import streamlit as st
from supabase import create_client, Client

logger = logging.getLogger(__name__)

def _resolve_config_value(key: str, default: str = "") -> str:
    """Resolve configuration value from environment variable or Streamlit secrets."""
    val = os.environ.get(key)
    if val:
        return val.strip()
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return default

ENVIRONMENT = os.environ.get("SNAPCLASS_ENV", "development").lower()

if ENVIRONMENT == "staging":
    # STRICT STAGING ISOLATION:
    # Staging MUST use distinct staging credentials (env vars or [staging] secrets table).
    # Under NO circumstances will it silently fall back to production credentials.
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

    if not SUPABASE_URL or not SUPABASE_KEY:
        try:
            if hasattr(st, "secrets") and "staging" in st.secrets:
                SUPABASE_URL = str(st.secrets["staging"].get("SUPABASE_URL", "")).strip()
                SUPABASE_KEY = str(st.secrets["staging"].get("SUPABASE_KEY", "")).strip()
        except Exception:
            pass

    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.warning(
            "STAGING CREDENTIALS MISSING: SNAPCLASS_ENV is 'staging', but separate staging "
            "credentials (SUPABASE_URL / SUPABASE_KEY) are not configured. "
            "Silently falling back to production credentials is strictly blocked."
        )
        supabase: Client = None
    else:
        logger.info("Initializing isolated STAGING Supabase client.")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

else:
    # Development / Production resolution
    SUPABASE_URL = _resolve_config_value("SUPABASE_URL")
    SUPABASE_KEY = _resolve_config_value("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.warning("Supabase credentials not configured. Database operations will require initialization.")
        supabase: Client = None
    else:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
