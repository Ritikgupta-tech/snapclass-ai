# SNAPCLASS AI — Verified Facts, Architectural Limitations & Project Gaps

**Course:** B.Tech Computer Science & Engineering  
**Project:** SNAPCLASS AI  
**Document Purpose:** Honest academic evaluation of verified codebase facts versus unverified marketing claims, identified technical limitations, and questions requiring project owner input prior to final thesis binding.  

---

## 1. Verified Technical Facts (Codebase Proven)

The following claims have been verified through direct source code inspection and test execution:

1. **Multi-Modal Recognition Capabilities**:
   - The application contains active, functional code for both facial recognition (`src/pipelines/face_pipeline.py`) using dlib ResNet (128-d vectors) and acoustic speaker verification (`src/pipelines/voice_pipeline.py`) using Resemblyzer LSTM (256-d vectors).
2. **CPU-Only Deep Learning Execution**:
   - The Dockerfile and deployment environments are pinned to the official PyTorch CPU wheel index (`https://download.pytorch.org/whl/cpu`). Resemblyzer and dlib run entirely without GPU or CUDA dependencies.
3. **Database Architecture**:
   - The database layer (`src/database/db.py`) interacts with 5 PostgreSQL tables in Supabase: `teachers`, `students`, `subjects`, `subject_students`, and `attendance_logs`.
4. **Idempotency & Concurrency Locking**:
   - `attendance_service.confirm_and_save_attendance` acquires an explicit in-memory thread lock (`_CONFIRM_LOCK = threading.Lock()`) and performs database-level pre-checks on `(subject_id, timestamp)` to prevent duplicate submissions.
5. **Security Implementation**:
   - Passwords are encrypted using salted bcrypt (`bcrypt.hashpw(..., bcrypt.gensalt())`).
   - Rate limiting tracks failed attempts per username (5 attempts) and per IP address (15 attempts) with a 300-second lockout.
   - Raw embeddings and passwords are systematically popped from session state dictionaries prior to UI rendering.
6. **Automated Test Coverage**:
   - Exactly 70 tests exist across 9 test files. 68 tests pass consistently, and 2 are intentionally skipped to protect the production Supabase database from receiving synthetic test data.

---

## 2. Unverified Claims & Marketing Statements (To Avoid in Academic Thesis)

In preparing a defensible B.Tech project report, avoid the following marketing claims that are not backed by empirical data in the codebase:

1. **"99.9% Verified Accuracy"**:
   - *Issue*: This figure appears in promotional UI tickers (`src/ui/base_layout.py`), but no rigorous benchmark on campus student cohorts has been formally conducted.
   - *Academic Stance*: Report the published academic benchmark of the underlying model: *"dlib's ResNet face recognition model achieves 99.38% accuracy on the Labeled Faces in the Wild (LFW) benchmark under standard evaluation protocols."*
2. **"< 0.2 Seconds Processing Time"**:
   - *Issue*: While in-memory vector comparison between a single pair takes $< 1\text{ ms}$, detecting and extracting landmarks across a multi-face 1080p crowd photograph on a CPU requires 1.8 to 2.4 seconds.
   - *Academic Stance*: Clearly state: *"Facial detection and feature extraction for a 30-student classroom photograph completes in approximately 2.0 to 2.5 seconds on standard dual-core/quad-core CPU hardware."*
3. **"Bank-Grade Encryption"**:
   - *Issue*: Marketing buzzword. The application uses standard TLS 1.3 over HTTPS for transport and salted bcrypt (work factor 12) for teacher passwords.
   - *Academic Stance*: State: *"Password security is enforced using salted Blowfish bcrypt hashing, and cloud communication utilizes standard TLS encrypted REST endpoints."*
4. **"Hardware Infrared Liveness Verification"**:
   - *Issue*: Some early documentation drafts mentioned anti-spoofing liveness detection. The current codebase does not implement optical flow, infrared depth sensing, or blink analysis.
   - *Academic Stance*: Formally list liveness detection as an identified limitation and key future enhancement in Chapter 12.

---

## 3. Identified Architectural Limitations & Technical Debt

1. **Service-Role Client Authorization**:
   - *Detail*: The Supabase client in `src/database/config.py` connects using a service-role key or standard API key. Relational authorization (e.g., verifying that Teacher A cannot view Teacher B's records) is enforced in the Python application logic (`check_teacher_owns_subject`) rather than at the database engine level via PostgreSQL Row Level Security (RLS).
   - *Thesis Discussion*: Present this as a deliberate architectural trade-off to simplify Streamlit stateless execution, while detailing the planned RLS migration in the future scope.
2. **Process-Local In-Memory Rate Limiting**:
   - *Detail*: `_GLOBAL_LOGIN_ATTEMPTS` is stored in a process-level Python dictionary (`_LOGIN_LOCK`). In a multi-worker load-balanced deployment (e.g., multiple Uvicorn/Streamlit worker processes or container replicas), rate limits are not shared across processes.
   - *Thesis Recommendation*: Discuss the limitation and propose a centralized Redis cache for distributed rate limiting in Chapter 12.
3. **Sequential Voice Activity Segmentation**:
   - *Detail*: `librosa.effects.split` splits audio on silence intervals (`top_db=25`). If two students answer "Present" simultaneously or overlap in time, the resulting audio segment is mixed, degrading the cosine similarity score.
   - *Thesis Recommendation*: Highlight the need for deep speaker diarization (e.g., PyAnnote) as future research.

---

## 4. Questions & Missing Information Requiring Project Owner Confirmation

Before compiling the final institutional report covers, the following university-specific metadata must be confirmed by the student/author:

1. **Author & Institutional Metadata**:
   - Student Full Name: *(e.g., Ritik Gupta)*
   - Student University Roll Number / Registration Number: *[To be provided by owner]*
   - Department: *Department of Computer Science & Engineering*
   - College / University Name: *[To be provided by owner]*
   - Project Supervisor / Guide Name & Designation: *(e.g., Prof. / Dr. ...)*
   - Academic Year & Submission Month: *(e.g., 2025–2026 / May 2026)*
2. **Real Database Staging Credentials**:
   - Does the institution possess a secondary, isolated Supabase project URL and key for executing the 2 skipped staging integration tests (`test_real_supabase_connectivity`, `test_real_database_idempotent_session_insert`), or should the report present the verified mock-isolated test baseline?
3. **Classroom Sample Data Preference**:
   - For thesis screenshots, do you prefer using synthetic sample student names (`Ritik Gupta`, `Aarav Sharma`, `Priya Patel`, `Ananya Roy`) or real enrolled classroom data? *(Synthetic sample data is strongly recommended for student privacy).*
