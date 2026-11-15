# SNAPCLASS AI — Security Architecture & Data Protection Guide

**Document Version**: 2.0.0  
**Classification**: Application Security Specification  

---

## 1. Security Overview

SNAPCLASS AI handles educational records and biometric representations. This document outlines the security architecture, threat model, implemented protective controls, and operational constraints governing the platform.

---

## 2. Threat Model & Mitigations

| Threat Category | Potential Attack Vector | Implemented Mitigation |
|---|---|---|
| **Credential Attacks** | Password guessing / brute-force on instructor login | Bcrypt hashing, strict password complexity (min 8 chars, mixed case, number), and automated rate-limiting lockout after 5 consecutive failed attempts. |
| **Biometric Spoofing** | Presentation of 2D photographs or recorded audio to camera | Transparent limitation disclosure: 2D web camera capture lacks hardware IR/depth liveness. FaceID is paired with institutional instructor review. |
| **Cross-Subject Leakage** | Students from unrelated classes being matched in a course | Strict roster scoping: AI pipelines match face and voice vectors **only** against students actively enrolled in the selected subject. |
| **Data Exposure** | Leakage of password hashes or biometric arrays in UI state | Database queries explicitly exclude sensitive columns (`password`, `face_embedding`, `voice_embedding`) during standard user sessions. |
| **Attendance Tampering** | Replay or duplicate submissions causing attendance inflation | Idempotency tokens per session (`session_id`) and backend teacher ownership verification prior to database commits. |

---

## 3. Biometric Data Handling

### 3.1 Vectorization vs Raw Storage
- SNAPCLASS AI **does not store raw classroom photographs or recorded student voice files in the persistent database**.
- During registration, uploaded photos and audio recordings are processed in-memory:
  - Faces are translated into 128-dimensional Euclidean metric embeddings via dlib's ResNet model.
  - Voices are translated into 256-dimensional speaker embeddings via Resemblyzer.
- Only the derived numeric arrays are stored in Supabase PostgreSQL columns. Raw media streams are discarded immediately following vector extraction.

### 3.2 Candidate Matching Scoping
- In previous versions, facial classification ran against all students globally across the entire database.
- In version 2.0.0, candidate matching is strictly constrained to `get_enrolled_students_for_subject(subject_id, include_embeddings=True)`.
- If a subject has 25 enrolled students, the pipeline compares input encodings strictly against those 25 reference vectors. Unenrolled students or strangers are classified as `UNKNOWN` and surfaced in a dedicated alert.

### 3.3 Confidence Calibration & Manual Review
- To prevent false attendance, matches are partitioned into three confidence tiers:
  1. **High Confidence** ($d \le 0.55$ for face; $\text{similarity} \ge 0.72$ for voice): Suggested as Present.
  2. **Needs Review** ($0.55 < d \le 0.65$ for face; $0.58 \le \text{similarity} < 0.72$ for voice): Flagged as "Review Needed" for instructor inspection.
  3. **Unknown / Unmatched** ($d > 0.65$ for face; $\text{similarity} < 0.58$ for voice): Counted as unknown faces; student marked Absent.
- The instructor has complete authority to toggle any student's status via the interactive data editor prior to confirmation.

---

## 4. Authentication & Session Security

### 4.1 Password Policy
Instructor passwords must satisfy the following criteria:
- Minimum length of 8 characters.
- At least one uppercase letter (`[A-Z]`).
- At least one lowercase letter (`[a-z]`).
- At least one digit (`[0-9]`).

### 4.2 Rate Limiting
- Failed login attempts are tracked per username.
- If 5 consecutive failures occur within a 5-minute window, the account is locked for 300 seconds.
- Lockout status and remaining cooldown seconds are presented to the user.

### 4.3 Safe Logout & State Purging
- When an instructor or student clicks "Sign Out", `logout()` purges all credentials, user profiles, uploaded photo queues, audio buffers, and active session tokens from `st.session_state`.

---

## 5. Authorization & Database Access Scoping

- Every attendance persistence call executes `check_teacher_owns_subject(teacher_id, subject_id)` before writing records.
- Even if a client session is modified, records cannot be inserted into subjects belonging to another instructor.
- Student profile endpoints restrict access to the authenticated student's enrolled courses and attendance logs.
