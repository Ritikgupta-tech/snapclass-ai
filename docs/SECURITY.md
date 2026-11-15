# SNAPCLASS AI — Security Architecture & Threat Model

**Document Version**: 2.2.0  
**Status**: Independently Verified & Hardened  

---

## 1. Security Architecture & Boundary Model

SNAPCLASS AI implements a defense-in-depth security model designed specifically for educational institution SaaS environments.

```mermaid
flowchart TD
    Client["Browser / Client Session"] -->|TLS 1.3 / HTTPS| App["Streamlit Application Server"]
    
    subgraph "Application Security Boundary"
        App --> RateLimit["Composite Rate Limiter (IP + Username)"]
        RateLimit --> AuthSvc["Auth Service (Bcrypt + Role Checks)"]
        AuthSvc --> SessionMgr["Session State Isolation (Teacher / Student)"]
        SessionMgr --> ScopedBio["Biometric Scoping & Ambiguity Detector"]
        ScopedBio --> AttService["Attendance Service (Mutex Lock + Idempotency)"]
    end
    
    subgraph "Data Storage Boundary"
        AttService -->|PostgREST (Service Role)| Supabase["Supabase PostgreSQL 15"]
        Supabase --> Tables["teachers / students / subjects / logs"]
    end
```

---

## 2. Authentication & Credential Security

1. **Password Hashing**: Passwords are never stored in plaintext. They are salted and hashed using standard `bcrypt` with work factor 12.
2. **Credential Stripping**: Functions `db_create_teacher` and `db_teacher_login` explicitly strip the `password` column before returning objects to callers or saving into `st.session_state`.
3. **Password Policy**: Enforces minimum 8 characters, at least one uppercase letter, one lowercase letter, and one number.
4. **Role Isolation**: Both `teacher_screen()` and `student_screen()` verify that `st.session_state.is_logged_in` is True AND that `st.session_state.user_role` matches the expected role (`"teacher"` vs `"student"`), preventing cross-role session contamination.
5. **Student FaceID Authentication**: Requires `HIGH_CONFIDENCE` match ($\text{Euclidean distance} \le 0.55$). If a face match is ambiguous (`NEEDS_REVIEW`), login is denied with an advisory message to protect account boundaries.

---

## 3. Rate Limiting Architecture

- **Scope**: Process-wide in-memory rate limiting enforced across all active Streamlit sessions in the server process.
- **Concurrency Safety**: Synchronized using `threading.Lock()` to eliminate race conditions between concurrent requests.
- **Composite Tracking**:
  - **Username Tracker**: Limits failed login attempts per username (maximum 5 attempts).
  - **IP Address Tracker**: Inspects client IP via `st.context.ip_address` (maximum 15 failed attempts across all usernames from the same IP) to prevent distributed dictionary spraying.
  - **Lockout Duration**: 15 minutes (900 seconds).
- **Honest Architectural Classification**: This rate limiter operates in process memory. It survives browser tab resets and page reloads, but does **not** persist across process restarts or distribute across independent multi-instance container replicas. In single-instance Streamlit deployments, it provides robust brute-force mitigation without adding Redis infrastructure overhead.

---

## 4. Authorization & Database Access Model

- **Supabase Key Analysis**: Verification of `.streamlit/secrets.toml` revealed that `SUPABASE_KEY` is a **`service_role` key**. In Supabase PostgreSQL, `service_role` bypasses Row Level Security (RLS) entirely.
- **Application-Layer Enforcement**:
  - Because RLS is bypassed by the client key, **all tenant isolation and ownership checks are strictly enforced in the Python service layer**.
  - `check_teacher_owns_subject(teacher_id, subject_id)` is executed on both session preparation and attendance confirmation.
  - `confirm_and_save_attendance` validates that every student ID in the submission payload is actively enrolled in the target subject before inserting records.
  - Raw biometric vectors (`face_embedding`, `voice_embedding`) are stripped from student profile queries unless explicitly needed by the pipeline.

---

## 5. Attendance Data Integrity & Idempotency

1. **Thread-Safe Mutex**: `_CONFIRM_LOCK` synchronizes `_CONFIRMED_SESSION_IDS` to block rapid double-clicks and concurrent browser tabs.
2. **Database Existence Check**: Verifies `(subject_id, timestamp)` against Supabase prior to writing, preventing duplicate submissions even if the server restarted.
3. **Payload Deduplication**: Pre-write deduplication guarantees that each enrolled student receives at most one record per session, preventing corrupted rosters.
4. **PostgreSQL Exception Translation**: Catches database unique constraint violations (code `23505`) and returns a clean, user-friendly duplicate response.

---

## 6. Biometric Security & Verification Boundaries

1. **Roster Scoping**: Biometric candidate comparisons are strictly filtered to students enrolled in the specific subject (`subject_students`), eliminating cross-course false positives.
2. **Twin & Close-Distance Ambiguity Guard**:
   - In `face_pipeline.py`, if the top candidate and runner-up candidate have a distance difference $< 0.05$, status is downgraded from `HIGH_CONFIDENCE` to `NEEDS_REVIEW`.
   - In `voice_pipeline.py`, if the top speaker and runner-up speaker have a cosine similarity difference $< 0.05$, status is downgraded to `NEEDS_REVIEW`.
3. **False Absence Prevention**:
   - If classroom photos contain 0 detectable faces, analysis halts with an error.
   - If classroom audio matches 0 enrolled students, analysis halts with an error.
   - The system never marks 100% of enrolled students absent when recognition models fail to detect biometrics.
4. **Evaluation Disclaimer**: Pre-trained Resemblyzer and dlib models provide robust metric similarity, but have not undergone proprietary accuracy benchmark verification on consented campus datasets. Resemblyzer silence-based splitting (`librosa.effects.split`) provides voice activity segmentation, not multi-speaker conversational diarization.
