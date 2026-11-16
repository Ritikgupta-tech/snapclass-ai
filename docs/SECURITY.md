# SNAPCLASS AI — Security Architecture & Threat Model

**Document Version**: 2.3.0  
**Status**: Independently Audited & Staging Hardened  

---

## 1. Security Architecture & Boundary Model

SNAPCLASS AI implements a multi-tier defense-in-depth security model:

```mermaid
flowchart TD
    Client["Browser / Client Session"] -->|HTTPS / WSS| App["Streamlit Application Server"]
    
    subgraph "Application Security Boundary"
        App --> RateLimit["Composite Rate Limiter (IP + Username Tracker)"]
        RateLimit --> AuthSvc["Auth Service (Bcrypt + Role Checks)"]
        AuthSvc --> SessionMgr["Session State Isolation (Teacher / Student)"]
        SessionMgr --> ScopedBio["Biometric Scoping & Ambiguity Guards"]
        ScopedBio --> AttService["Attendance Service (Mutex Lock + Roster Validation)"]
    end
    
    subgraph "Data Storage Boundary"
        AttService -->|PostgREST (Backend Server-Side)| Supabase["Supabase PostgreSQL 15"]
        Supabase --> Tables["teachers / students / subjects / logs"]
    end
```

---

## 2. Authentication, Role Isolation & Abuse Testing

1. **Password Hashing**: Salted and hashed using standard `bcrypt` with work factor 12.
2. **Credential Sanitization**: Functions `create_teacher` and `teacher_login` in `src/database/db.py` explicitly delete the `password` column before returning objects to callers or saving into `st.session_state`. Passwords are never written to logs or tracebacks.
3. **Role Enforcement**:
   - `teacher_screen()` strictly validates `st.session_state.is_logged_in is True` AND `st.session_state.user_role == "teacher"`.
   - `student_screen()` strictly validates `st.session_state.is_logged_in is True` AND `st.session_state.user_role == "student"`.
4. **Student FaceID Login**: Restricted strictly to `HIGH_CONFIDENCE` matches ($\text{Euclidean distance} \le 0.55$). Borderline matches (`NEEDS_REVIEW`) prompt for realignment and re-capture rather than granting portal access.
5. **Abuse Verification**:
   - `test_missing_credentials_handled_gracefully`: Verifies empty, whitespace, and null credentials return clean user messages without tracebacks.
   - `test_cross_subject_unauthorized_teacher_injection`: Verifies a teacher cannot confirm attendance for a subject they do not own.

---

## 3. Rate Limiting Architecture

- **Scope**: Process-wide in-memory rate limiting enforced across all active Streamlit sessions in the server process.
- **Concurrency Safety**: Synchronized using `threading.Lock()` to eliminate race conditions between concurrent requests.
- **Composite Tracking**:
  - **Username Tracker**: Maximum 5 failed attempts per username $\to$ 15-minute lockout.
  - **IP Address Tracker**: Maximum 15 failed attempts per client IP (`st.context.ip_address`) $\to$ 15-minute lockout across all usernames (mitigates dictionary spraying).
- **Architectural Classification**: Operates in process memory. Survives browser tab resets and page reloads, but does not survive process restarts or distribute across independent multi-instance container replicas. Redis is not configured in this repository; adding external Redis infrastructure was avoided to minimize deployment overhead for single-instance staging.

---

## 4. Supabase Authorization & Credential Handling

- **Key Role Analysis**: Verification of `.streamlit/secrets.toml` confirmed that `SUPABASE_KEY` is a **`service_role` key**. In Supabase PostgreSQL, `service_role` bypasses Row Level Security (RLS) entirely.
- **Application-Layer Enforcement**:
  - Because RLS is bypassed by the client key, **all tenant isolation, teacher ownership checks (`check_teacher_owns_subject`), and student privacy boundaries are enforced at the Python application service layer**.
  - `confirm_and_save_attendance` verifies that every student ID in the submission payload is actively enrolled in the target subject before inserting records.
  - Raw biometric vectors (`face_embedding`, `voice_embedding`) are stripped from student profile queries unless explicitly needed by the pipeline.
- **Feasibility of Restricted Database Role**:
  - Current users are managed in application tables (`public.teachers`, `public.students`) rather than Supabase Auth (`auth.users`).
  - Switching immediately to an `anon` key would cause PostgREST to evaluate queries as unauthenticated (`auth.uid() = NULL`), breaking all existing student and teacher queries.
  - **Production Recommendation**: For future releases, migrate authentication to Supabase Auth (`gotrue`) to enable native RLS policies with `anon` keys. For Staging, server-side `service_role` client with service-layer validation remains the stable path.

---

## 5. Attendance Data Integrity & Idempotency

1. **Thread-Safe Mutex**: `_CONFIRM_LOCK` synchronizes `_CONFIRMED_SESSION_IDS` to block rapid double-clicks and concurrent browser tabs.
2. **Database Existence Check**: Verifies `(subject_id, timestamp)` against Supabase prior to writing, preventing duplicate submissions even if the server restarted.
3. **Payload Deduplication**: Pre-write deduplication guarantees that each enrolled student receives at most one record per session, preventing corrupted rosters.
4. **PostgreSQL Exception Translation**: Catches database unique constraint violations (code `23505`) and returns a clean, user-friendly duplicate response.
