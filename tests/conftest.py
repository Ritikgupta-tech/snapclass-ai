"""
Global Pytest Configuration and Environment Setup.
Ensures repository root is always present on sys.path across all CI/CD runners,
local environments, and test runners.
"""

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
