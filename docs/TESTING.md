# SNAPCLASS AI — Comprehensive QA & Performance Test Report

**Document Version**: 2.3.0  
**Status**: 63 / 65 Passed, 2 Skipped (Real DB Staging Guarded), 0 Failures  
**Execution Time**: 13.98s  

---

## 1. Test Execution Summary

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\DELL\Desktop\SNAPCLASS

tests/integration/test_attendance_service.py    7 PASSED  [ 10%]
tests/integration/test_real_db_workflow.py      2 SKIPPED [ 13%]
tests/integration/test_subject_service.py       3 PASSED  [ 18%]
tests/unit/test_face_pipeline.py                8 PASSED  [ 30%]
tests/unit/test_security_auth.py                9 PASSED  [ 44%]
tests/unit/test_validators.py                  19 PASSED  [ 73%]
tests/unit/test_voice_pipeline.py               9 PASSED  [ 87%]
tests/workflows/test_e2e_attendance_flow.py     1 PASSED  [ 89%]
tests/workflows/test_regression_bugs.py         7 PASSED  [100%]

================= 63 passed, 2 skipped, 4 warnings in 13.98s ==================
```

---

## 2. Test Category Breakdown & Mock Separation

| Category | File Path | Tests | Mode | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Validators** | `tests/unit/test_validators.py` | 19 | Unit | ✅ Passed |
| **Face Pipeline** | `tests/unit/test_face_pipeline.py` | 8 | Unit | ✅ Passed |
| **Voice Pipeline** | `tests/unit/test_voice_pipeline.py` | 9 | Unit | ✅ Passed |
| **Auth & Abuse Security** | `tests/unit/test_security_auth.py` | 9 | Unit | ✅ Passed |
| **Subject Service** | `tests/integration/test_subject_service.py` | 3 | Integration (Mocked) | ✅ Passed |
| **Attendance Service** | `tests/integration/test_attendance_service.py` | 7 | Integration (Mocked) | ✅ Passed |
| **Real Database Staging** | `tests/integration/test_real_db_workflow.py` | 2 | Real DB (Staging Guard) | ⏭️ Skipped |
| **Regression Fixes** | `tests/workflows/test_regression_bugs.py` | 7 | Regression (Mocked) | ✅ Passed |
| **Full Lifecycle E2E** | `tests/workflows/test_e2e_attendance_flow.py` | 1 | E2E (Mocked Store) | ✅ Passed |
| **Total** | | **65** | | **63 Passed / 2 Skipped** |

> [!NOTE]
> **Mock vs Real Database Separation**:
> Tests in `test_real_db_workflow.py` are strictly guarded by `SNAPCLASS_STAGING_TEST_RUN=true` and `SNAPCLASS_ENV=staging`. They skip automatically when executed in environments without an isolated staging database, preventing accidental writes or load against production.

---

## 3. Measured Performance Benchmarks

All performance metrics were measured locally using high-resolution hardware timers (`time.perf_counter()`) and `tracemalloc`:

| Performance Metric | Measured Value | Architectural Assessment |
| :--- | :---: | :--- |
| **Cold Start / Full App Import** | `20,132.78 ms` (20.1s) | Typical for heavy ML frameworks (Torch, Numba, SciPy, Streamlit) on Windows |
| **Database Read Roundtrip (Supabase Cloud)** | `993.20 ms` | Normal for remote cloud PostgreSQL roundtrip |
| **Dlib Face Models Initialization** | `2,144.61 ms` (2.1s) | 100MB+ model weights loaded; cached via `@st.cache_resource` on subsequent runs |
| **Resemblyzer Voice Encoder Initialization** | `183.55 ms` | Fast PyTorch LSTM initialization; cached via `@st.cache_resource` |
| **Face Detection Pass (300×300 RGB Image)** | `66.87 ms` | Sub-100ms detection pass with HOG frontal detector |
| **Traced Memory (Current / Peak)** | `158.65 MB / 158.90 MB` | Lean footprint well within standard 1GB staging container limits |
| **Concurrent Submission Contention (5 Threads)** | `3.97 ms` total | Exactly 1 thread succeeded; 4 threads locked/rejected; avg thread latency `0.04 ms` |

---

## 4. UI Runtime Verification via Agent API

The Streamlit web application was executed headlessly and validated using the Streamlit Agent API (`/_stcore/agent/interact`):
- Navigation from landing page to Instructor portal.
- Form field population for instructor authentication.
- Rate-limiting error banner display upon intentional invalid attempts.
- Navigation transition to Student FaceID sign-in portal.
- All views render without duplicate widget key warnings or styling breakages.
