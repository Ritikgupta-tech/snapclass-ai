# SNAPCLASS AI — Comprehensive Academic Project Research Master

**Project Name:** SNAPCLASS AI (Smart Classroom Attendance Management System)  
**Academic Degree:** Bachelor of Technology (B.Tech) in Computer Science & Engineering  
**Project Category:** AI/ML-Powered Web Application, Multi-Modal Biometrics, Cloud SaaS  
**Document Classification:** Master Technical Research & Codebase Audit Reference  
**Audit Date:** November 2026  

---

## 1. Executive Summary & Problem Context

Traditional classroom attendance in higher education institutions relies primarily on paper-based roll calls or manual spreadsheet entry. In university lecture halls containing 60 to 120 students, calling attendance manually consumes between 10 to 15 minutes per lecture—equating to roughly 15% to 25% of instructional time lost. Furthermore, manual systems are inherently vulnerable to proxy attendance ("buddy punching"), transcription errors, and physical register loss.

While secondary automated alternatives have emerged (RFID card swipe terminals, fingerprint biometric scanners, and static QR codes), each presents severe practical impediments:
- **RFID systems** require expensive hardware readers per classroom and do not prevent students from carrying colleagues' cards.
- **Fingerprint scanners** create long physical queues at classroom doorways, exhibit hygiene issues, and introduce substantial maintenance costs.
- **Static QR codes** projected on lecture screens are frequently photographed, shared via messaging applications, and scanned remotely by absent students.

**SNAPCLASS AI** is architected to address these shortcomings through a **non-intrusive, multi-modal biometric classroom attendance platform**. It combines:
1. **Passive Panoramic Facial Recognition**: An instructor captures a single panoramic or wide-angle photograph of the lecture hall from any standard device. The system simultaneously detects, localizes, extracts 128-dimensional deep metric embeddings, and identifies all present enrolled students within seconds using dlib ResNet-based metric learning.
2. **Acoustic Voice Check-in**: An alternative or complementary vocal verification pipeline utilizing a 3-layer LSTM Deep Speaker Encoder (Resemblyzer) that generates 256-dimensional vocal embeddings from spoken roll-call responses, matched via normalized cosine similarity.
3. **Dynamic QR Code Joining**: Instant student enrollment via cryptographically clean QR codes and direct URL invitation routing powered by `segno`.
4. **Human-in-the-Loop Review**: An interactive confirmation data grid allowing instructors full authority to inspect, verify, override, and confirm records before idempotent database persistence.
5. **Privacy-by-Design Compliance**: Strict privacy preservation where raw student photographs and audio streams are processed in transient memory and discarded immediately, persisting only encrypted mathematical vectors.

---

## 2. Complete Repository & Codebase Structural Inventory

The application follows an adapted Model-View-Controller (MVC) and modular service-layer pattern on top of Python 3.12/3.14 and Streamlit 1.67.

```text
C:\Users\DELL\Desktop\SNAPCLASS/
├── .github/
│   └── workflows/
│       └── ci.yml                          # Continuous Integration workflow (Ubuntu, Python 3.12, Pytest)
├── .streamlit/
│   ├── config.toml                         # Streamlit server, browser, and theme configuration
│   └── secrets.toml.example                # Template for Supabase URL, service key, and environment flags
├── docs/                                   # Existing architectural and audit specifications
│   └── college-project-report/             # Generated academic project report deliverables
├── src/
│   ├── __init__.py                         # Core package marker
│   ├── components/                         # Modular Streamlit UI widgets and dialog modals
│   │   ├── __init__.py
│   │   ├── dialog_add_photo.py             # Classroom photo upload and camera capture modal
│   │   ├── dialog_attendance_results.py    # Interactive data editor for reviewing attendance drafts
│   │   ├── dialog_auto_enroll.py           # Auto-registration helper dialog
│   │   ├── dialog_create_subject.py        # Academic course creation modal
│   │   ├── dialog_enroll.py                # Student course code enrollment modal
│   │   ├── dialog_share_subject.py         # High-resolution QR code display modal
│   │   ├── dialog_voice_attendance.py      # Audio capture and voice recognition modal
│   │   ├── footer.py                       # Institutional footer component
│   │   ├── header.py                       # Brand navigation header with live status telemetry
│   │   └── subject_card.py                 # Academic subject presentation card with KPI metrics
│   ├── config/
│   │   ├── __init__.py
│   │   └── app_config.py                   # Global constants, biometric thresholds, and URL schemes
│   ├── database/
│   │   ├── __init__.py
│   │   ├── config.py                       # Environment-isolated Supabase client factory
│   │   └── db.py                           # PostgREST data access layer, queries, and bcrypt hashing
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── face_pipeline.py                # dlib 128-d face embedding extraction & Euclidean matching
│   │   └── voice_pipeline.py               # Resemblyzer 256-d speaker encoder & cosine similarity
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── home_screen.py                  # Public landing portal with value pillars & role entrypoints
│   │   ├── student_screen.py               # Student portal: face sign-in, profile, and attendance history
│   │   └── teacher_screen.py               # Faculty portal: course manager, attendance taker, history
│   ├── services/
│   │   ├── __init__.py
│   │   ├── attendance_service.py           # Attendance draft coordination, mutex locking, and saving
│   │   ├── auth_service.py                 # Teacher/student auth, bcrypt checks, and rate limiting
│   │   └── subject_service.py              # Course lifecycle, QR generation, student dashboard metrics
│   ├── ui/
│   │   ├── __init__.py
│   │   └── base_layout.py                  # Global CSS layout engine, typography, and responsive media
│   └── validators/
│       ├── __init__.py
│       ├── audio_validators.py             # Duration, size, and header validation for audio payloads
│       ├── image_validators.py             # Dimension normalization, RGB conversion, and bounds checks
│       └── input_validators.py             # Regex sanitization for passwords, usernames, and codes
├── tests/                                  # Comprehensive automated test suite
│   ├── conftest.py                         # Pytest global path resolution marker
│   ├── integration/
│   │   ├── test_attendance_service.py      # Idempotency, deduplication, and authorization tests
│   │   ├── test_real_db_workflow.py        # Real database staging tests (guarded by isolation flag)
│   │   └── test_subject_service.py         # Course creation and student aggregation tests
│   ├── unit/
│   │   ├── test_face_pipeline.py           # Metric distance, ambiguity gating, and runner-up margin
│   │   ├── test_security_auth.py           # Bcrypt hashing, lockout tracking, and IP spraying tests
│   │   ├── test_validators.py              # Input, image, and audio boundary validation tests
│   │   └── test_voice_pipeline.py          # Cosine similarity and speech segmentation unit tests
│   └── workflows/
│       ├── test_e2e_attendance_flow.py     # Complete end-to-end multi-role attendance lifecycle
│       └── test_regression_bugs.py         # Regression tests for audio crash, single-student, and exports
├── .dockerignore                           # Docker build context exclusion list
├── .gitignore                              # Git version control ignore rules
├── app.py                                  # Primary Streamlit entrypoint and global route dispatcher
├── Dockerfile                              # Multi-platform Python 3.12 Debian Bookworm container definition
├── packages.txt                            # System-level apt dependencies for Debian/Streamlit Cloud
├── pytest.ini                              # Pytest configuration file with pythonpath and testpaths
└── requirements.txt                        # Pinned Python package dependencies
```

---

## 3. Detailed Technology Stack & Library Audit

| Technology / Library | Exact Version in Environment | Primary Purpose | Source Code Usage & Justification |
| :--- | :--- | :--- | :--- |
| **Python** | `3.12 LTS` (Docker/CI) / `3.14.6` (Local) | Core Programming Language | Provides asynchronous execution, typed data structures, and mathematical ecosystem. |
| **Streamlit** | `1.67.0` | Frontend UI & Interactive Runtime | Web presentation framework providing reactive state re-runs, camera/audio inputs, dialogs, and metrics. |
| **Supabase Client** | `2.34.1` | Cloud Database ORM / REST Client | Python client interfacing with cloud-hosted PostgreSQL 15 via HTTPS/PostgREST. |
| **PostgreSQL** | `15.x` (Supabase managed) | Relational Database Engine | Stores relational entities: teachers, students, subjects, enrollment associations, and logs. |
| **dlib / dlib-bin** | `20.0.1.post1` | Face Detection & Landmark Extraction | C++ machine learning library utilizing HOG + Linear SVM for detection and deep ResNet for face embeddings. |
| **face_recognition_models** | `0.3.0` | Pre-trained Metric Weights | Ships pre-trained 68-point shape predictor (`sp.dat`) and 128-d metric ResNet weights (`facerec.dat`). |
| **Resemblyzer** | `0.1.4` | Speaker Voice Verification | Pre-trained 3-layer LSTM neural network producing 256-d speaker embeddings from spectrograms. |
| **PyTorch (torch)** | `2.15.0` (CPU-Only) | Deep Learning Tensor Engine | Backing tensor engine executing the Resemblyzer voice encoder forward pass without GPU requirements. |
| **librosa** | `1.0.1` | Audio Processing & Speech Splitting | Acoustic analysis library utilized for 16kHz resampling and `librosa.effects.split` silence detection. |
| **soundfile / soxr** | `0.14.0` / `1.1.0` | Audio I/O & High-Quality Resampling | Reads diverse audio container formats (WAV, OGG, WebM) into normalized float arrays. |
| **webrtcvad-wheels** | `2.0.14.post1` | Voice Activity Detection | WebRTC VAD engine identifying voiced vs unvoiced frames in audio buffers. |
| **NumPy** | `2.5.4` | Vector & Matrix Computations | Performs Euclidean norm computation (`np.linalg.norm`), array slicing, and cosine dot products. |
| **Pandas** | `3.1.0` | Tabular Data Structuring & Review | Converts attendance dictionaries to DataFrames for `st.data_editor` and handles CSV export formatting. |
| **scikit-learn** | `1.9.1` | Machine Learning Utilities | Provides cosine distance metrics, cross-validation utilities, and statistical data scaling. |
| **bcrypt** | `5.0.0` | Secure Password Hashing | Enforces salted Blowfish password hashing (`bcrypt.gensalt()`) with work factor 12 for teacher accounts. |
| **Segno** | `1.6.6` | QR Code Generation Engine | Pure-Python ISO/IEC 18004 QR code generator producing error-corrected (Level H) PNG vectors. |
| **Pillow (PIL)** | `13.0.0` | Digital Image Pre-processing | Decodes camera snapshots, validates aspect ratios, converts color channels (RGBA/BGR to RGB), downscales. |
| **Docker** | `29.8.0` / Engine v29 | Application Containerization | Encapsulates Debian Bookworm Linux environment, apt dependencies, unprivileged user, and health probes. |
| **Pytest** | `9.2.0` | Automated Verification Suite | Headless test runner orchestrating unit, integration, security, and regression tests. |

---

## 4. Architectural Deep Dive: Biometric Pipelines

### 4.1 Facial Recognition Pipeline (`src/pipelines/face_pipeline.py`)

1. **Model Loading & Resource Caching**:
   `load_dlib_models()` is decorated with `@st.cache_resource`, ensuring that the 100MB+ pre-trained neural network weights (`dlib.get_frontal_face_detector()`, `dlib.shape_predictor()`, and `dlib.face_recognition_model_v1()`) are loaded exactly once per worker process.
2. **Detection & Alignment**:
   Input images are validated via `src/validators/image_validators.py`, ensuring maximum dimension does not exceed 1920 pixels (preserving aspect ratio via Lanczos downsampling) and ensuring 3-channel RGB format. Faces are detected using HOG (Histogram of Oriented Gradients) with an upsample factor of 1 (`FACE_DETECTION_UPSAMPLE = 1`). For each detected bounding box, 68 facial landmarks (jawline, eyebrows, nose bridge, eyes, lip contours) are extracted to apply affine transformation, normalizing roll, pitch, and yaw.
3. **128-Dimensional Metric Vector Computation**:
   The aligned face chip is passed through the pre-trained ResNet deep metric network, producing a 128-dimensional unit hypersphere vector $\mathbf{x} \in \mathbb{R}^{128}$.
4. **Subject-Scoped Euclidean Distance Classification**:
   Instead of comparing against a global student directory of thousands of candidates, SNAPCLASS AI scopes candidate matching strictly to students enrolled in the active subject:
   $$\mathcal{D}(\mathbf{x}, \mathbf{y}) = \|\mathbf{x} - \mathbf{y}\|_2 = \sqrt{\sum_{i=1}^{128} (x_i - y_i)^2}$$
5. **Dual-Threshold Gating with Ambiguity Guard**:
   - **High Confidence**: If $\min(\mathcal{D}) \le 0.55$ (`FACE_DISTANCE_THRESHOLD`), the face is matched to the top student.
   - **Needs Review**: If $0.55 < \min(\mathcal{D}) \le 0.65$ (`FACE_AMBIGUOUS_THRESHOLD`), the face is flagged for instructor review.
   - **Ambiguity Downgrade Rule**: If the difference between the minimum distance and runner-up candidate is less than 0.05 ($d_2 - d_1 < 0.05$), the system automatically downgrades the status to `NEEDS_REVIEW` to prevent misattribution between lookalikes.
   - **Unknown**: If $\min(\mathcal{D}) > 0.65$, the face is marked as unmapped.

### 4.2 Voice Recognition Pipeline (`src/pipelines/voice_pipeline.py`)

1. **Audio Validation & Preprocessing**:
   Raw audio bytes captured via Streamlit's audio input are validated by `validate_audio_payload()` (checking payload size $\le 10\text{ MB}$, valid audio header, duration between 0.5s and 60.0s). The stream is decoded via `librosa.load` at a fixed sampling rate of 16,000 Hz (`VOICE_SAMPLE_RATE = 16000`).
2. **Non-Silent Utterance Segmentation (Voice Activity Detection)**:
   The classroom recording is split into discrete speech segments using `librosa.effects.split(audio, top_db=25)`. Segments shorter than 0.4 seconds ($\text{duration} < 0.4 \times sr$) are rejected as acoustic transient noise.
3. **256-Dimensional Speaker Vector Extraction**:
   Each speech segment is preprocessed via `resemblyzer.preprocess_wav` and passed through the pre-trained 3-layer LSTM Voice Encoder. The resulting 256-dimensional output vector $\mathbf{u} \in \mathbb{R}^{256}$ is $L_2$-normalized:
   $$\hat{\mathbf{u}} = \frac{\mathbf{u}}{\|\mathbf{u}\|_2}$$
4. **Normalized Cosine Similarity Scoring**:
   Speaker verification compares the segment embedding $\hat{\mathbf{u}}$ against stored enrolled student embeddings $\hat{\mathbf{v}}$:
   $$\mathcal{S}(\hat{\mathbf{u}}, \hat{\mathbf{v}}) = \frac{\hat{\mathbf{u}} \cdot \hat{\mathbf{v}}}{\|\hat{\mathbf{u}}\|_2 \|\hat{\mathbf{v}}\|_2} = \cos(\theta)$$
5. **Acoustic Gating & Ambiguity Rejection**:
   - **High Confidence**: If $\max(\mathcal{S}) \ge 0.72$ (`VOICE_CONFIDENCE_THRESHOLD`), matched to top candidate.
   - **Needs Review**: If $0.58 \le \max(\mathcal{S}) < 0.72$ (`VOICE_AMBIGUOUS_THRESHOLD`), marked for teacher verification.
   - **Acoustic Ambiguity Downgrade**: If top score and second-best score differ by less than 0.05 ($s_1 - s_2 < 0.05$), downgraded to `NEEDS_REVIEW`.
   - **Unknown / Rejection**: If $\max(\mathcal{S}) < 0.58$, student is not identified from the utterance.

---

## 5. Security, Concurrency & Data Integrity Architecture

### 5.1 Defense-in-Depth Authentication & Rate Limiting (`src/services/auth_service.py`)
- **Password Policy**: Enforced by `validate_password()` requiring $\ge 8$ characters, at least one uppercase letter, and at least one numeric digit.
- **Salted Bcrypt Hashing**: Passwords stored as irreversible Blowfish hashes with automated unique salting (`bcrypt.gensalt()`).
- **Process-Wide Rate Limiting**:
  - Implements a thread-safe mutex (`_LOGIN_LOCK = threading.Lock()`) protecting `_GLOBAL_LOGIN_ATTEMPTS`.
  - Blocks targeted brute-force attacks after 5 consecutive failed attempts per username (`MAX_LOGIN_ATTEMPTS = 5`) for 300 seconds (`LOCKOUT_DURATION_SECONDS = 300`).
  - Blocks distributed credential stuffing / dictionary spraying by tracking client IP (`st.context.ip_address`), locking out any IP exceeding 15 failed attempts across usernames.
- **Biometric Leak Prevention**:
  `auth_service.logout()` purges all session state keys and forces garbage collection. `get_all_students()` and `get_student_by_id()` default to `include_embeddings=False` to prevent transmitting 128-d or 256-d vectors into UI state unless required for model inference.

### 5.2 Concurrency & Idempotent Database Commitment (`src/services/attendance_service.py`)
- **Double-Click & Race Condition Prevention**:
  When an instructor confirms an attendance session, the service acquires an in-memory lock (`_CONFIRM_LOCK`) and checks `session_id` against `_CONFIRMED_SESSION_IDS`. Concurrent duplicate requests are rejected immediately.
- **Database-Level Idempotency Check**:
  `check_attendance_session_exists(subject_id, timestamp)` executes an indexed query on `attendance_logs` to ensure that no attendance records for the identical subject and timestamp exist in PostgreSQL before attempting an insert.
- **Server-Side Referential Integrity Validation**:
  Before saving, all student IDs in the payload are verified against `get_enrolled_students_for_subject(subject_id)`. Any foreign student ID injected into the client request payload causes immediate transaction abortion.
- **Payload Deduplication**:
  The payload is pre-processed with a hash set on `(subject_id, student_id, timestamp)`, guaranteeing that a student cannot be logged twice in the same session.
- **Graceful Error Translation**:
  PostgreSQL error code `23505` (unique constraint violation) is captured and translated into human-readable notifications.

---

## 6. Testing & Quality Assurance Verification Summary

The test harness is implemented in Pytest 9.2.0 and validated across 9 specialized test modules.

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0 -- venv\scripts\python.exe
rootdir: C:\Users\DELL\Desktop\SNAPCLASS
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.16.0, platformdirs-4.14.5
collected 70 items

tests/integration/test_attendance_service.py: 7 passed
tests/integration/test_real_db_workflow.py: 2 skipped (Staging safety gate)
tests/integration/test_subject_service.py: 3 passed
tests/unit/test_face_pipeline.py: 8 passed
tests/unit/test_security_auth.py: 14 passed
tests/unit/test_validators.py: 19 passed
tests/unit/test_voice_pipeline.py: 9 passed
tests/workflows/test_e2e_attendance_flow.py: 1 passed
tests/workflows/test_regression_bugs.py: 7 passed

======================== 68 passed, 2 skipped in 6.43s ========================
```

### Staging Isolation Rationale
The 2 skipped tests in `test_real_db_workflow.py` (`test_real_supabase_connectivity`, `test_real_database_idempotent_session_insert`) are protected by a safety gate (`@pytest.mark.skipif(not IS_STAGING_CONFIGURED)`). This guarantees that local test runs and GitHub Actions CI runs **never execute mutations or synthetic inserts against the live production database instance** (`ref: rwuejklxdjjhathhwdga`).

---

## 7. Current Project Implementation Status

| Capability / Module | Status | Verified Implementation Location |
| :--- | :--- | :--- |
| **Teacher Registration & Login** | Implemented & Verified | `src/services/auth_service.py`, `src/screens/teacher_screen.py` |
| **Student Face Sign-In (FaceID)** | Implemented & Verified | `src/screens/student_screen.py`, `src/pipelines/face_pipeline.py` |
| **Student Biometric Profile Enrollment**| Implemented & Verified | `src/screens/student_screen.py`, `src/database/db.py` |
| **Subject / Course Creation** | Implemented & Verified | `src/services/subject_service.py`, `src/components/dialog_create_subject.py`|
| **Subject QR Code Generation** | Implemented & Verified | `src/services/subject_service.py` (`segno` Level H PNG) |
| **Student URL / QR One-Tap Join** | Implemented & Verified | `app.py` (`st.query_params['join-code']`), `subject_service.py` |
| **Classroom Panoramic Photo Roll Call**| Implemented & Verified | `src/services/attendance_service.py`, `src/pipelines/face_pipeline.py` |
| **Voice-Activated Spoken Roll Call** | Implemented & Verified | `src/services/attendance_service.py`, `src/pipelines/voice_pipeline.py` |
| **Interactive Attendance Review Grid**| Implemented & Verified | `src/components/dialog_attendance_results.py` (`st.data_editor`) |
| **Attendance Confirmation & Mutex** | Implemented & Verified | `src/services/attendance_service.py` (`threading.Lock`) |
| **Duplicate Prevention & Idempotency** | Implemented & Verified | `src/services/attendance_service.py`, `src/database/db.py` |
| **Student Attendance History & Stats**| Implemented & Verified | `src/services/subject_service.py`, `src/screens/student_screen.py` |
| **Teacher Attendance Overview & History**| Implemented & Verified | `src/services/attendance_service.py`, `src/screens/teacher_screen.py` |
| **CSV Export of Attendance Summaries**| Implemented & Verified | `src/screens/teacher_screen.py` (Pandas CSV generation) |
| **Bcrypt Salted Password Hashing** | Implemented & Verified | `src/database/db.py` (`bcrypt.hashpw`) |
| **Rate Limiting & Lockout Engine** | Implemented & Verified | `src/services/auth_service.py` (Username & IP spray defense) |
| **Responsive Dark Layout Engine** | Implemented & Verified | `src/ui/base_layout.py`, `.streamlit/config.toml` |
| **Multi-Platform Dockerization** | Implemented & Verified | `Dockerfile` (Python 3.12, Debian Bookworm Slim, Non-root user)|
| **Continuous Integration CI Pipeline** | Implemented & Verified | `.github/workflows/ci.yml`, `pytest.ini` |
| **Hardware Infrared Liveness Detection**| Planned / Proposed | Not implemented (requires depth/NIR hardware sensor). |
| **Speaker Diarization (Multi-talker)**| Planned / Proposed | Audio is segmented on silence; true conversational diarization is proposed. |
| **Database Row Level Security (RLS)** | Partially Implemented | App-level authorization verified; PostgreSQL RLS policies documented in migration plan. |
