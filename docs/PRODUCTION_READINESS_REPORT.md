# SNAPCLASS AI — Phase 3 Production Readiness & Independent Audit Report

**Report Date**: 2026-11-15  
**Auditor**: Senior Software Architect & Lead Security/QA Engineer  
**Branch**: `feature/snapclass-premium-upgrade`  
**Classification**: **READY FOR STAGING** (Condition: Apply Supabase Phase 1 DDL before multi-worker production deployment)  

---

## 1. Executive Summary

| Evaluation Domain | Audit Classification | Key Findings & Hardening Implemented |
| :--- | :---: | :--- |
| **Git & Tree Integrity** | **PASS** | Clean working tree; atomic local commits; zero secret exposure; Option B retained. |
| **Test Automation** | **PASS (61/61)** | 61 automated tests pass in 8.72s (Unit, Integration, Regression, and E2E Lifecycle). |
| **Attendance Data Integrity** | **PASS (Staging)** | Thread-safe mutex lock, pre-write student deduplication, server-side roster verification, and DB collision handling. |
| **Authentication & RBAC** | **PASS** | Composite IP + Username rate limiting; password hashes stripped; strict `user_role` screen validation. |
| **Database & Supabase** | **CONDITIONALLY READY** | Read-only inspection verified live schema. Client uses `service_role` key (RLS bypassed). Phase 1 unique index SQL prepared. |
| **Biometric Pipelines** | **PASS (Documented)** | Candidate scoping; twin/close-distance downgrading; zero-detection false absence halts; diarization limits documented. |
| **UI & UX Quality** | **PASS** | Streamlit Linear/Stripe design system; responsive layouts; Agent API verified; RFC 4180 CSV export. |
| **Dependency Ecosystem** | **PASS (With Warnings)** | Python 3.14.6 runs cleanly. Upstream warnings in `face_recognition_models` and `resemblyzer` documented. Python 3.11/3.12 recommended for Docker. |

---

## 2. Attendance Data Integrity Audit

### 2.1 Concurrency & Idempotency Analysis
- **Double-Click & Concurrent Tabs**: Guarded by `_CONFIRM_LOCK` synchronizing `_CONFIRMED_SESSION_IDS` in `src/services/attendance_service.py`. Concurrent requests within the same process are serialized.
- **Application Restarts**: Guarded by `check_attendance_session_exists(subject_id, timestamp)`. If the application restarts, subsequent confirmation attempts are rejected because the session timestamp already exists in Supabase.
- **Duplicate Student Records in Payload**: If an altered client payload or UI glitch submits duplicate student records for a single session, pre-write deduplication in `confirm_and_save_attendance` and `create_attendance` strips duplicates, preserving only one record per student.
- **Server-Side Roster Verification**: `confirm_and_save_attendance` queries `get_enrolled_students_for_subject` to verify that submitted student IDs are legally enrolled in the subject, rejecting unauthorized student injection attempts.
- **Multi-Worker Database Atomicity**:
  - The live `attendance_logs` table currently lacks a unique constraint on `(subject_id, student_id, timestamp)`.
  - While single-instance deployments are fully protected by application locks, distributed multi-worker deployments (e.g., multiple Docker containers behind an ALB) require PostgreSQL-level uniqueness.
  - A zero-downtime SQL script (`docs/DATABASE_MIGRATION_PLAN.md` Phase 1) has been prepared to add `uq_attendance_logs_subject_student_ts`. Application code already catches PostgreSQL error `23505` to gracefully return a friendly duplicate submission message.

---

## 3. Security & Access Control Findings

### 3.1 Supabase Service Role Discovery
- Direct inspection revealed that `SUPABASE_KEY` in `.streamlit/secrets.toml` is a **`service_role` key**.
- Because the `service_role` key bypasses PostgreSQL Row Level Security (RLS), RLS policies defined in database files are not evaluated by PostgREST.
- **Remediation**: All access controls, teacher ownership checks (`check_teacher_owns_subject`), and student boundary restrictions are enforced strictly in the Python application service layer.

### 3.2 Rate Limiting
- Replaced basic username-only tracking with a **composite rate limiter**:
  - Limits failed attempts per username (5 max).
  - Limits failed attempts per client IP address via `st.context.ip_address` (15 max across all usernames).
  - Prevents distributed dictionary spraying and incognito session bypass.
  - Protected with `threading.Lock()`.
  - Accurately documented as an in-memory process-level limiter (no Redis infrastructure overhead).

### 3.3 Session & Screen Boundary Hardening
- Direct navigation in `app.py`, `teacher_screen.py`, and `student_screen.py` validates `user_role` explicitly.
- Student FaceID login now strictly requires `HIGH_CONFIDENCE` ($\le 0.55$). Borderline detections (`NEEDS_REVIEW`) prompt for realignment and re-capture rather than granting portal access.

---

## 4. Biometric Recognition Evaluation

### 4.1 Face Recognition (`face_pipeline.py`)
- Employs 128-dimensional deep metric embeddings with 1-to-1 Euclidean distance matching against enrolled subject candidates.
- **Ambiguity Guard**: When the top candidate and runner-up candidate have a distance difference $< 0.05$, the system automatically downgrades the status to `NEEDS_REVIEW` to prevent misidentifying lookalikes or twins.
- **False Absence Guard**: Halts immediately if zero faces are found in classroom photos.

### 4.2 Voice Recognition (`voice_pipeline.py`)
- Employs 256-dimensional Resemblyzer speaker embeddings with cosine similarity scoring.
- **Ambiguity Guard**: When the top candidate and runner-up candidate have a cosine score difference $< 0.05$, status is downgraded to `NEEDS_REVIEW`.
- **False Absence Guard**: If audio contains speech but matches 0 enrolled students, processing halts with an error instead of generating an all-absent review table.
- **Diarization Disclaimer**: Resemblyzer uses silence-based energy segmentation (`librosa.effects.split`), which provides voice activity detection for sequential responses, not full conversational speaker diarization.

---

## 5. Dependency & Environment Analysis

- **Runtime**: Python 3.14.6 on Windows x86_64.
- **Verification**: Core machine learning libraries (`dlib-bin 20.0.1`, `numpy 2.5.4`, `pandas 3.1.0`, `librosa 1.0.1`, `resemblyzer 0.1.4`, `scikit-learn 1.9.1`, `streamlit 1.67.0`) execute without functional errors.
- **Deprecation Warnings**:
  1. `face_recognition_models` imports deprecated `pkg_resources`.
  2. `resemblyzer` imports deprecated `scipy.ndimage.morphology.binary_dilation`.
- **Production Recommendation**: For production containerization (Docker), deploy on **Python 3.11 or 3.12 LTS** on Debian Bullseye/Bookworm where pre-built wheels are mature and upstream warnings are minimized.

---

## 6. QA Test Suite Execution

All 61 tests executed and passed locally:

- `tests/integration/test_attendance_service.py`: 7 passed
- `tests/integration/test_subject_service.py`: 3 passed
- `tests/unit/test_face_pipeline.py`: 8 passed
- `tests/unit/test_security_auth.py`: 7 passed
- `tests/unit/test_validators.py`: 19 passed
- `tests/unit/test_voice_pipeline.py`: 9 passed
- `tests/workflows/test_e2e_attendance_flow.py`: 1 passed (14 steps)
- `tests/workflows/test_regression_bugs.py`: 7 passed

**Execution time**: `8.72s`  
**Passed**: 61 / 61  
**Failed**: 0  

---

## 7. Production Readiness Decision & Staging Checklist

### Status: READY FOR STAGING

### Staging Deployment Checklist:
1. Deploy application artifact to staging server running Python 3.11/3.12 or 3.14.
2. Execute Phase 1 database migration script from `docs/DATABASE_MIGRATION_PLAN.md` in Supabase SQL Editor:
   ```sql
   CREATE UNIQUE INDEX IF NOT EXISTS uq_attendance_logs_subject_student_ts 
   ON attendance_logs(subject_id, student_id, timestamp);
   ```
3. Perform end-to-end user acceptance testing (UAT) with pilot instructors.
4. Schedule Phase 2 relational migration (`attendance_sessions` / `attendance_records`) during a scheduled maintenance window.
