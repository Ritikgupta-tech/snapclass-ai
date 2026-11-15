# SNAPCLASS AI — Changelog & Version History

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.3.0] - 2026-11-15 (Phase 4: Staging Preparation & Release Engineering)

### Added
- **Multi-Platform Dockerfile**: Production-ready container specification based on `python:3.12-slim-bookworm` with system libraries for dlib/librosa, non-root user `appuser`, and health check probe.
- **Dockerignore Configuration**: Created `.dockerignore` excluding `.git`, `.venv`, secrets, tests, and temporary caches.
- **Dual Credential Resolution**: Updated `src/database/config.py` to resolve configuration from environment variables (`SNAPCLASS_ENV`, `SUPABASE_URL`, `SUPABASE_KEY`) with fallback to Streamlit secrets.
- **Mock vs Real Database Separation**: Added `tests/integration/test_real_db_workflow.py` guarded by `SNAPCLASS_STAGING_TEST_RUN=true` to separate real database testing from mocked unit/integration tests.
- **Abuse Testing Suite**: Added tests for missing credentials, invalid parameter handling, and cross-subject unauthorized teacher access.
- **Accurate Performance Benchmarking**: Documented measured latencies for cold start, model loading, memory consumption, and thread contention.

---

## [2.2.0] - 2026-11-15 (Phase 3: Distributed Safety & Final Engineering Audit)

### Added
- **Composite Rate Limiting**: Added client IP address tracking (`st.context.ip_address`) alongside username tracking with thread-safe mutex (`_LOGIN_LOCK`).
- **Biometric Ambiguity Protection**:
  - Added runner-up candidate distance gap check in `face_pipeline.py`: downgrades status to `NEEDS_REVIEW` if distance difference is $< 0.05$.
  - Added runner-up speaker score gap check in `voice_pipeline.py`: downgrades status to `NEEDS_REVIEW` if similarity difference is $< 0.05$.
- **Roster & Payload Deduplication**: Pre-write deduplication in `confirm_and_save_attendance` and `create_attendance`.
- **Server-Side Roster Enrollment Check**: Validates submitted student IDs against enrolled course roster.
- **PostgreSQL Error Translation**: Catches database unique violation `23505` and formats a user-friendly duplicate response.
- **False Absence Prevention**: `prepare_voice_attendance_session` halts with an error if 0 enrolled students are recognized.

---

## [2.1.0] - 2026-11-15 (Phase 2: Independent Verification & Security Hardening)

### Added
- **Dual-Tier Idempotency**: Process-level memory mutex coupled with database timestamp check (`check_attendance_session_exists`).
- **Full E2E 14-Step Lifecycle Test**: Comprehensive automated workflow covering instructor registration, subject creation, student enrollment, multi-modal analysis, instructor review overrides, attendance confirmation, duplicate rejection, and unenrollment history.

---

## [2.0.0] - 2026-11-15 (Phase 1: Architecture Modernization & Option B Retained)

### Added
- Modern Streamlit dark/light SaaS theme in `.streamlit/config.toml`.
- Modular service layer: `src/services/auth_service.py`, `src/services/subject_service.py`, `src/services/attendance_service.py`.
- Validation layer: `src/validators/input_validators.py`, `src/validators/image_validators.py`, `src/validators/audio_validators.py`.
- Interactive attendance review data table with manual teacher status overrides.
