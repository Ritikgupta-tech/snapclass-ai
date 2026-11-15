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

ENVIRONMENT = _resolve_config_value("SNAPCLASS_ENV", "development").lower()
SUPABASE_URL = _resolve_config_value("SUPABASE_URL")
SUPABASE_KEY = _resolve_config_value("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("Supabase credentials not configured. Database operations will require initialization.")
    supabase: Client = None  # Handled safely in db layer
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
