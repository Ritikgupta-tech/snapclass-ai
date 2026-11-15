# SNAPCLASS AI — Comprehensive QA Test Report

**Document Version**: 2.2.0  
**Status**: 61 / 61 Passing (0 Failures, 4 Upstream Deprecation Warnings)  
**Execution Time**: 8.72s  

---

## 1. Test Execution Summary

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\DELL\Desktop\SNAPCLASS

tests/integration/test_attendance_service.py   7 PASSED  [ 11%]
tests/integration/test_subject_service.py      3 PASSED  [ 16%]
tests/unit/test_face_pipeline.py               8 PASSED  [ 29%]
tests/unit/test_security_auth.py               7 PASSED  [ 40%]
tests/unit/test_validators.py                 19 PASSED  [ 72%]
tests/unit/test_voice_pipeline.py              9 PASSED  [ 86%]
tests/workflows/test_e2e_attendance_flow.py    1 PASSED  [ 88%]
tests/workflows/test_regression_bugs.py        7 PASSED  [100%]

======================= 61 passed, 4 warnings in 8.72s ========================
```

---

## 2. Test Category Breakdown

| Category | File Path | Tests | Status |
| :--- | :--- | :---: | :---: |
| **Validators** | `tests/unit/test_validators.py` | 19 | ✅ Passed |
| **Face Pipeline** | `tests/unit/test_face_pipeline.py` | 8 | ✅ Passed |
| **Voice Pipeline** | `tests/unit/test_voice_pipeline.py` | 9 | ✅ Passed |
| **Auth & Security** | `tests/unit/test_security_auth.py` | 7 | ✅ Passed |
| **Subject Service** | `tests/integration/test_subject_service.py` | 3 | ✅ Passed |
| **Attendance Service** | `tests/integration/test_attendance_service.py` | 7 | ✅ Passed |
| **Regression Fixes** | `tests/workflows/test_regression_bugs.py` | 7 | ✅ Passed |
| **Full Lifecycle E2E** | `tests/workflows/test_e2e_attendance_flow.py` | 1 | ✅ Passed |
| **Total** | | **61** | **100% Passed** |

---

## 3. Detailed Verification Matrix

### 3.1 Attendance Data Integrity & Idempotency
- `test_idempotent_confirmation`: Verifies that re-submitting with the same `session_id` is rejected in memory.
- `test_db_level_duplicate_timestamp_rejected`: Verifies that re-submitting after a restart triggers database timestamp collision rejection.
- `test_unauthorized_teacher_rejected`: Verifies that a teacher cannot confirm attendance for a subject they do not own.
- `test_duplicate_student_records_in_payload_deduplicated`: Verifies that duplicate student records in submission payloads are deduplicated before DB write.
- `test_unregistered_student_in_attendance_rejected`: Verifies that attempting to record attendance for an un-enrolled student is rejected.
- `test_db_unique_constraint_violation_handled_gracefully`: Verifies that PostgreSQL `23505` unique violation is caught and translated to a clean user message.

### 3.2 Biometric Recognition & Candidate Scoping
- `test_exact_face_match` / `test_ambiguous_face_match` / `test_unknown_face`: Tests canonical Euclidean thresholds ($0.55$ and $0.62$).
- `test_scoped_candidate_isolation`: Verifies that candidate embeddings from Subject A cannot match students in Subject B.
- `test_similar_candidates_downgraded_to_needs_review`: Verifies that two candidates with distance gap $< 0.05$ are downgraded to `NEEDS_REVIEW`.
- `test_similar_voice_speakers_downgraded_to_needs_review`: Verifies that two voice speakers with similarity gap $< 0.05$ are downgraded to `NEEDS_REVIEW`.
- `test_voice_session_zero_matches_halts_gracefully`: Verifies that when 0 enrolled students are recognized in audio, processing halts rather than recording everyone absent.

### 3.3 Authentication & Rate Limiting
- `test_rate_limiting_lockout_after_max_attempts`: Verifies 5-attempt threshold triggers 15-minute lockout.
- `test_rate_limiting_persists_across_streamlit_session_restarts`: Verifies that rate limiting survives session state resets.
- `test_rate_limiting_composite_ip_spraying_lockout`: Verifies that client IP spraying across multiple usernames triggers lockout.
- `test_logout_purges_authenticated_state`: Verifies all authenticated keys are deleted on sign-out.

---

## 4. UI Runtime Verification via Agent API

The Streamlit web application was executed headlessly and validated using the Streamlit Agent API (`/_stcore/agent/interact`):
- Navigation from landing page to Instructor portal.
- Form field population for instructor authentication.
- Rate-limiting error banner display upon intentional invalid attempts.
- Navigation transition to Student FaceID sign-in portal.
- All views render without duplicate widget key warnings or styling breakages.
