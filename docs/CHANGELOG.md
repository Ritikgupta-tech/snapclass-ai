# Changelog — SNAPCLASS AI

All notable changes to the SNAPCLASS AI project are documented in this file.

---

## [2.0.0] - 2026-11-15 — Production-Grade SaaS Transformation

### 🌟 Added
- **Centralized Configuration System (`src/config/app_config.py`)**:
  - Dynamically configured canonical application URL (`APP_URL`) with fallback to production domain.
  - Standardized biometric thresholds for facial Euclidean distance and speaker cosine similarity.
  - Audio and image upload constraints (size, duration, resolution).
- **Comprehensive Validation Tier (`src/validators/`)**:
  - `input_validators.py`: Username, password complexity, subject code regex, and string sanitization.
  - `audio_validators.py`: Multi-format audio validation via `soundfile`, non-empty check, duration bounds.
  - `image_validators.py`: Standardized RGB conversion and downsampling for high-res images (max 1920px).
- **Service Layer Architecture (`src/services/`)**:
  - `auth_service.py`: Instructor authentication, password hashing with bcrypt, rate limiting (5 attempts lockout), and session state purge.
  - `subject_service.py`: Subject creation with duplicate code collision prevention, student enrollment/unenrollment, dashboard statistics, and QR code generation.
  - `attendance_service.py`: Orchestrates multi-photo face analysis, voice recognition, editable review tables, session roll-ups, and idempotent database persistence.
- **Premium Design System & Theme (`.streamlit/config.toml`, `src/ui/base_layout.py`)**:
  - Modern typography using `Inter` and `JetBrains Mono`.
  - Balanced neutral palette (dark slate / crisp light) with refined indigo/violet accents.
  - Subtle borders, clean container cards, and responsive metrics.
- **Public SaaS Landing Page (`src/screens/home_screen.py`)**:
  - Hero header with value proposition.
  - Role-specific access cards with Material Symbols (`:material/school:`, `:material/co_present:`).
  - 3-step workflow explanation and institutional privacy disclosure.
- **Automated Test Suite (`tests/`)**:
  - 46 automated tests with Pytest 9.2.0 spanning unit, integration, and regression suites with 100% pass rate.
- **Technical Documentation (`docs/`)**:
  - `PROJECT_AUDIT.md`: Exhaustive audit of all existing files, features, and defect categorizations.
  - `ARCHITECTURE.md`: High-level system architecture, multi-tier diagrams, and workflow blueprints.
  - `SECURITY.md`: Biometric protection, threat model, candidate scoping, and access control.
  - `DATABASE_MIGRATION_PLAN.md`: Current schema analysis, target session modeling, and rollback SQL.
  - `TESTING.md`: Complete test coverage report and runtime agent API verification evidence.

---

### 🐛 Fixed (P0 / P1 / P2 / P3 Defects)
- **ISSUE-P0-01 (Voice NoneType Crash)**: Added defensive validation in `dialog_voice_attendance.py` and `audio_validators.py` preventing `AttributeError: 'NoneType' object has no attribute 'read'`.
- **ISSUE-P0-02 (Voice False Absent Logging)**: Prevented generating all-absent attendance records when audio recognition yields 0 matches or fails; added clear error feedback with retry options.
- **ISSUE-P0-03 (Subject Card Loop Closure Bug)**: Corrected loop indentation and closure bindings in `teacher_screen.py` so all subjects render their own cards and share buttons.
- **ISSUE-P0-04 (Face Pipeline Single-Class Crash & Global Unscoped Matching)**: Replaced unscoped global linear SVM with subject-scoped candidate distance matching; handles single-student rosters, multi-student rosters, and unknown faces cleanly.
- **ISSUE-P0-05 (Hardcoded Outdated Domain in QR Code)**: Eliminated hardcoded `snapclass-main.streamlit.app` and missing scheme; QR code now generates valid canonical URL with `https://`.
- **ISSUE-P0-06 (Photo Uploader & Camera Rerun Duplication)**: Fixed infinite file accumulation loop in `dialog_add_photo.py` with explicit import actions and queue tracking.
- **ISSUE-P0-07 (Duplicate Attendance Confirmation)**: Introduced session idempotency token in `attendance_service.py` to prevent duplicate writes on multi-click.
- **ISSUE-P0-08 (Duplicate Streamlit Element Keys)**: Resolved duplicate `key='loginbackbtn'` across screens, assigning distinct contextual keys.
- **ISSUE-P1-01 (Sensitive Credential & Biometric Exposure)**: Explicitly scoped database queries to omit password hashes and biometric embeddings from general user responses.
- **ISSUE-P1-02 (Unenforced Teacher Ownership Scoping)**: Added backend verification ensuring instructors can only record attendance for subjects they own.
- **ISSUE-P1-03 (Weak Password Policy)**: Enforced 8-character minimum, mixed case, and number requirements during instructor registration.
- **ISSUE-P2-01 (Full Database Scans in `get_all_students`)**: Replaced institutional scans with subject-scoped candidate queries.
- **ISSUE-P2-02 (Wholesale Cache Invalidation)**: Decoupled neural network model caches from student roster updates.
- **ISSUE-P2-03 (Classroom Photo Downsampling)**: Added automatic scaling to max 1920px, reducing face detection inference time by >90%.
- **ISSUE-P3-01 (Informal Discord Theme & Font)**: Replaced Discord-purple `#5865F2`, neon pink `#EB459E`, and `'Climate Crisis'` block font with a modern SaaS aesthetic.
- **ISSUE-P3-03 (Editable Attendance Review)**: Upgraded static dataframe in `dialog_attendance_results.py` to an interactive `st.data_editor` allowing instructors to adjust attendance statuses before saving.
- **ISSUE-P3-04 (Empty State Failures)**: Replaced blank dashboard voids with informative, beautifully designed empty states.
