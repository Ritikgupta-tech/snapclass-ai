# SNAPCLASS AI — Changelog & Version History

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.2.0] - 2026-11-15 (Phase 3: Distributed Safety & Final Engineering Audit)

### Added
- **Composite Rate Limiting**: Added client IP address tracking (`st.context.ip_address`) alongside username tracking with thread-safe mutex (`_LOGIN_LOCK`) to block distributed dictionary spraying attacks.
- **Biometric Ambiguity Protection**:
  - Added runner-up candidate distance gap check in `face_pipeline.py`: downgrades status to `NEEDS_REVIEW` if distance difference is $< 0.05$.
  - Added runner-up speaker score gap check in `voice_pipeline.py`: downgrades status to `NEEDS_REVIEW` if similarity difference is $< 0.05$.
- **Roster & Payload Deduplication**: Added pre-write deduplication in `confirm_and_save_attendance` and `create_attendance` ensuring at most one record per student.
- **Server-Side Roster Enrollment Check**: `confirm_and_save_attendance` validates that all submitted student IDs belong to the enrolled course roster.
- **PostgreSQL Error Translation**: Catches database unique violation `23505` and formats a user-friendly duplicate submission response.
- **False Absence Prevention**: `prepare_voice_attendance_session` halts with an error if 0 enrolled students are recognized, preventing false absent records.
- **Test Suite Expansion**: Added 8 new automated tests covering IP rate limiting, biometric twin ambiguity, payload deduplication, roster verification, zero-match voice halting, and CSV export (61 tests total).

### Changed
- **Student FaceID Login Hardening**: Restricted student portal biometric authentication strictly to `HIGH_CONFIDENCE` ($\le 0.55$), blocking borderline matches.
- **Screen Role Verification**: Added strict `user_role` checks to `teacher_screen` and `student_screen` to prevent cross-role session contamination.

---

## [2.1.0] - 2026-11-15 (Phase 2: Independent Verification & Security Hardening)

### Added
- **Dual-Tier Idempotency**: Process-level memory mutex coupled with database timestamp check (`check_attendance_session_exists`).
- **Full E2E 14-Step Lifecycle Test**: Comprehensive automated workflow covering instructor registration, subject creation, student enrollment, multi-modal analysis, instructor review overrides, attendance confirmation, duplicate rejection, and unenrollment history.
- **Zero-Face Warning Guard**: Classroom photo analysis immediately warns and halts if zero faces are detected.

---

## [2.0.0] - 2026-11-15 (Phase 1: Architecture Modernization & Option B Retained)

### Added
- Modern Streamlit dark/light SaaS theme in `.streamlit/config.toml`.
- Modular service layer: `src/services/auth_service.py`, `src/services/subject_service.py`, `src/services/attendance_service.py`.
- Validation layer: `src/validators/input_validators.py`, `src/validators/image_validators.py`, `src/validators/audio_validators.py`.
- Interactive attendance review data table with manual teacher status overrides.
- 46-test automated test suite.

### Fixed
- Fixed single-student crash in face recognition by migrating from multi-class SVM to 1-to-1 Euclidean distance metric matching.
- Fixed subject card loop closure bug where button callbacks shared loop variables.
- Fixed voice attendance `NoneType` crash on empty audio payloads.
- Fixed `subject_students` deletion typo in `src/database/db.py`.
