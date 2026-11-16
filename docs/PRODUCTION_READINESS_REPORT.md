# SNAPCLASS AI — Phase 4 Staging Readiness & Release Engineering Report

**Report Date**: 2026-11-15  
**Auditor Roles**: Principal Engineer, DevOps Architect, Database Security Engineer, QA Lead, Senior Python Developer  
**Branch**: `feature/snapclass-premium-upgrade`  
**Classification**: **`READY FOR ISOLATED STAGING`**  

---

## 1. Executive Summary

| Evaluation Domain | Audit Classification | Key Findings & Hardening Implemented |
| :--- | :---: | :--- |
| **Git & Tree Integrity** | **PASS** | Clean working tree; atomic local commits; zero secret exposure; Option B retained. |
| **Test Automation** | **PASS (63/65)** | 63 automated tests pass, 2 real-DB staging tests cleanly skipped when staging env absent. |
| **Attendance Integrity** | **READY FOR STAGING** | Thread-safe mutex lock, pre-write deduplication, server-side roster verification, and DB unique index prepared. |
| **Supabase Security** | **READY FOR STAGING** | Client uses `service_role` key (RLS bypassed). Service-layer authorization verified. Dual env/secrets resolver added. |
| **Docker & Linux** | **PASS** | `Dockerfile` (Python 3.12 Bookworm, non-root user, healthcheck probe) and `.dockerignore` created. |
| **Real vs Mock Tests** | **PASS** | Explicit separation in `test_real_db_workflow.py` guarded by `SNAPCLASS_STAGING_TEST_RUN=true`. |
| **Performance Benchmarks** | **MEASURED** | Cold start: 20.1s, DB read: 993ms, Dlib init: 2.1s, Voice init: 183ms, Peak RAM: 158.9MB, Contention: 3.97ms. |

---

## 2. Attendance Database Integrity & Session Model

### 2.1 Unique Index Evaluation: `(subject_id, student_id, timestamp)` vs `(session_id, student_id)`
- **Evaluation**: Relying on `timestamp` provides a basic guard, but can suffer from timestamp drift if a client generates a new timestamp on retry.
- **Stable Session Model**: A stable `session_id` (UUIDv4) is generated at session draft preparation. This ID remains identical across client retries and review overrides.
- **Pre-Migration Audit Result**:
  - Direct read-only inspection was executed on the live database:
  - Total `attendance_logs` rows: 3.
  - Duplicate rows found: **0**.
  - The database is clean and ready for index application without data loss.
- **Two-Phase Migration Scripts**:
  - **Phase 1 (Immediate Zero-Downtime)**: Creates `uq_attendance_logs_subject_student_ts` on the existing `attendance_logs` table.
  - **Phase 2 (Normalized Relational Model)**: Creates dedicated `attendance_sessions` and `attendance_records` tables with `uq_session_student UNIQUE (session_id, student_id)`.

---

## 3. Supabase Security & Credential Hygiene

- **Key Role Analysis**: The active `SUPABASE_KEY` is a `service_role` key. It bypasses RLS at the PostgREST layer.
- **Enforcement Boundary**: All access control, ownership verification, and student boundaries are enforced at the Python service layer.
- **Secret Safety**:
  - `SUPABASE_KEY` is never rendered in client templates, logs, or exports.
  - `src/database/config.py` now resolves credentials from OS environment variables (`SUPABASE_URL`, `SUPABASE_KEY`, `SNAPCLASS_ENV`) with fallback to `.streamlit/secrets.toml`.
  - Credentials in production and staging remain strictly decoupled.

---

## 4. Docker & Containerization Verification

- **Base Image**: `python:3.12-slim-bookworm`.
- **System Packages**: `build-essential`, `cmake`, `git`, `curl`, `libopenblas-dev`, `liblapack-dev`, `libx11-dev`, `libgtk-3-dev`, `libsndfile1`, `ffmpeg`.
- **Security**: Runs under unprivileged user `appuser` (UID 1001).
- **Health Check Probe**:
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
      CMD curl --fail http://localhost:8501/_stcore/health || exit 1
  ```
- **Context Exclusion**: `.dockerignore` prevents embedding `.git`, secrets, tests, or temporary files.

---

## 5. Performance Benchmarks

Hardware-measured benchmarks on Windows x86_64 host:

- **App Cold Start / Full Import**: `20,132.78 ms`
- **Database Read Roundtrip (Remote Cloud)**: `993.20 ms`
- **Dlib Face Models Initialization**: `2,144.61 ms`
- **Voice Encoder Initialization**: `183.55 ms`
- **Face Detector Pass (300×300 RGB)**: `66.87 ms`
- **Process Traced Memory (Current / Peak)**: `158.65 MB / 158.90 MB`
- **Concurrent Submission Contention (5 Threads)**: `3.97 ms` total (1 succeeded, 4 rejected/locked; average latency per thread `0.04 ms`)

---

## 6. Real vs Mock Test Classification

- **Unit & Mocked Integration Tests**: 63 tests pass locally without external dependencies.
- **Real Database Integration Tests**: 2 tests in `tests/integration/test_real_db_workflow.py` are explicitly skipped unless `SNAPCLASS_STAGING_TEST_RUN=true` and `SNAPCLASS_ENV=staging` are present, guaranteeing zero accidental writes against production.

---

## 7. Staging Release Decision & Exact Owner Steps

### Final Classification: `READY FOR ISOLATED STAGING`

### Exact Manual Steps Required from Project Owner:
1. **Create Staging Supabase Project**:
   - Create a separate, isolated Supabase project for staging (e.g., `snapclass-staging`).
   - Run the initial schema creation from `docs/DATABASE_MIGRATION_PLAN.md`.
2. **Apply Phase 1 Database Migration in Staging**:
   - Run `docs/DATABASE_MIGRATION_PLAN.md` Phase 1 SQL in the Staging Supabase SQL Editor:
     ```sql
     CREATE UNIQUE INDEX IF NOT EXISTS uq_attendance_logs_subject_student_ts 
     ON attendance_logs(subject_id, student_id, timestamp);
     ```
3. **Configure Staging Environment Variables / Secrets**:
   - Set `SNAPCLASS_ENV=staging`.
   - Set `SUPABASE_URL` and `SUPABASE_KEY` pointing to the staging Supabase project.
4. **Run Real Staging Database Tests**:
   ```bash
   SNAPCLASS_STAGING_TEST_RUN=true SNAPCLASS_ENV=staging pytest tests/integration/test_real_db_workflow.py -v
   ```
5. **Build and Deploy Staging Container**:
   ```bash
   docker build -t snapclass-ai:staging .
   docker run -p 8501:8501 --env-file .env.staging snapclass-ai:staging
   ```
