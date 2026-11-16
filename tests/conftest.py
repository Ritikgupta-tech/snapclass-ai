"""
Global Pytest Configuration and Environment Setup.
Ensures repository root is always present on sys.path across all CI/CD runners,
local environments, and test runners.
Also guarantees that if cloud credentials are absent (e.g. GitHub Actions runner),
a safe Mock Supabase client is attached so unmocked queries do not raise NoneType errors.
"""

import sys
import os
from unittest.mock import MagicMock

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Defensive CI safety fixture:
# If supabase client is None (running in CI without production credentials),
# attach a mock client so tests do not crash on NoneType attribute access.
try:
    import src.database.config as db_cfg
    if db_cfg.supabase is None:
        mock_supabase = MagicMock()
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = []
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = []
        mock_supabase.table.return_value.delete.return_value.execute.return_value.data = []
        mock_supabase.table.return_value.update.return_value.execute.return_value.data = []
        db_cfg.supabase = mock_supabase
        import src.database.db as db_mod
        db_mod.supabase = mock_supabase
except Exception:
    pass
