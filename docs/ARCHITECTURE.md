# SNAPCLASS AI — Architectural Specification

**Document Version**: 2.0.0  
**Status**: Production-Ready SaaS Architecture  
**Primary Framework**: Streamlit (Option B — Architecture Retained & Upgraded)  
**Database**: Supabase / PostgreSQL  

---

## 1. System Overview

SNAPCLASS AI is an intelligent attendance management platform engineered for universities, colleges, and training institutes. It replaces time-consuming manual roll calls with multi-modal AI verification (facial recognition and speaker voice identification), backed by strict instructor review and idempotent database recording.

```
                      +-----------------------------+
                      |       User Client           |
                      |  (Desktop / Mobile Browser) |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |       Streamlit Runtime     |
                      |       (app.py / UI)         |
                      +--------------+--------------+
                                     |
         +---------------------------+---------------------------+
         |                           |                           |
         v                           v                           v
+------------------+       +------------------+       +------------------+
|  Auth Service    |       |  Subject Service |       |Attendance Service|
+--------+---------+       +--------+---------+       +--------+---------+
         |                          |                          |
         +--------------------------+--------------------------+
                                    |
         +--------------------------+--------------------------+
         |                                                     |
         v                                                     v
+------------------+                                 +-------------------+
| Biometric ML     |                                 | Database Access   |
| Pipelines        |                                 | Layer (db.py)     |
| (dlib / Resembly)|                                 +---------+---------+
+------------------+                                           |
                                                               v
                                                     +-------------------+
                                                     | Supabase Cloud    |
                                                     | (PostgreSQL)      |
                                                     +-------------------+
```

---

## 2. Layered Architecture Design

The application follows a clean 5-tier architecture:

### 2.1 Presentation Tier (`src/screens/`, `src/components/`, `src/ui/`)
- **`app.py`**: Global router, page configuration (`layout="wide"`), query parameter listener (`join-code`), and session state baseline initializer.
- **`home_screen.py`**: Public landing page featuring brand identity, product workflow, feature highlights, and direct role-based entrypoints.
- **`teacher_screen.py`**: Instructor portal with overview metrics, subject cards, photo gallery, real-time face analysis, and searchable attendance history.
- **`student_screen.py`**: Student portal supporting FaceID camera authentication, profile registration, enrolled subjects view, and attendance log.
- **`src/components/`**: Modular modal dialogs for photo capture, audio roll-call, subject creation, QR generation, and attendance verification.
- **`src/ui/base_layout.py`**: Subdued, theme-compliant CSS enhancements complementing `.streamlit/config.toml`.

### 2.2 Validation Tier (`src/validators/`)
- **`input_validators.py`**: Regex and bounds validation for usernames, password complexity, subject codes, and string sanitization.
- **`audio_validators.py`**: Validates audio payload byte sizes, decodability via `soundfile`, non-empty streams, and duration bounds (0.5s – 60s).
- **`image_validators.py`**: Validates image payloads, converts various color profiles to standardized RGB, and resizes oversized classroom photos (max 1920px) to prevent memory overload.

### 2.3 Service Tier (`src/services/`)
- **`auth_service.py`**: Orchestrates instructor login/registration, password hashing via bcrypt, rate-limiting (5 attempts lockout), and clean session purging.
- **`subject_service.py`**: Manages subject creation with duplicate code prevention, student enrollment/unenrollment, dashboard statistics aggregation, and QR code generation with canonical URL resolution.
- **`attendance_service.py`**: Coordinates multi-image facial analysis and bulk audio recognition, structures editable review sessions, prevents duplicate submissions via session idempotency tokens, and formats attendance roll-ups.

### 2.4 Biometric Pipeline Tier (`src/pipelines/`)
- **`face_pipeline.py`**:
  - `load_dlib_models()`: Caches pre-trained shape predictor and recognition network at the process level using `@st.cache_resource`.
  - `get_face_embeddings()`: Computes 128-dimensional deep metric embeddings for all detected faces.
  - `analyze_classroom_photo()`: Performs 1-to-1 Euclidean distance matching against enrolled candidates of the specific subject. Classifies detections into High Confidence, Needs Review, or Unknown.
- **`voice_pipeline.py`**:
  - `load_voice_encoder()`: Caches Resemblyzer voice encoder.
  - `get_voice_embedding()`: Generates 256-dimensional normalized speaker embedding.
  - `process_bulk_audio()`: Splits classroom audio on non-silent speech segments and calculates cosine similarity against enrolled candidates.

### 2.5 Persistence Tier (`src/database/`)
- **`config.py`**: Supabase client connection configured via `.streamlit/secrets.toml`.
- **`db.py`**: Hardened database queries with explicit column selection, referential integrity checks, and sensitive field stripping.

---

## 3. Core Operational Workflows

### 3.1 Classroom Face Attendance Workflow
```
[Instructor] Uploads / Snaps Classroom Photos
      │
      ▼
[Image Validator] Resizes to max 1920px & converts to RGB
      │
      ▼
[Database] Retrieves ONLY enrolled students for selected subject (with face_embedding)
      │
      ▼
[Face Pipeline] Detects faces & computes 128-d embeddings
      │
      ▼
[Matcher] Computes Euclidean distance against enrolled candidates:
      ├── Distance <= 0.55  --> High Confidence Match (Present)
      ├── 0.55 < d <= 0.65  --> Marginal Match (Needs Review)
      └── Distance > 0.65   --> Unknown Face (Logged & Flagged)
      │
      ▼
[Review Dialog] Teacher inspects editable roster, overrides statuses if needed
      │
      ▼
[Attendance Service] Idempotent commit to Supabase with session ID lock
```

### 3.2 Subject Joining via QR Code
```
[Instructor] Creates Subject (e.g. CS101)
      │
      ▼
[Subject Service] Generates Canonical URL (https://<canonical-domain>/?join-code=CS101)
      │
      ▼
[Segno] Emits Crisp QR Code PNG (scale 8, border 2)
      │
      ▼
[Student] Scans QR with phone camera
      │
      ▼
[App Router] Detects ?join-code=CS101 in query params
      ├── If not authenticated: Directs student to FaceID sign-in
      └── If authenticated: Displays instant one-click course enrollment modal
```

---

## 4. Performance & Scalability Considerations

1. **Model Cache Separation**: Neural network weights (dlib 100MB model and Resemblyzer) remain permanently cached in memory via `@st.cache_resource`. They are never flushed when student rosters or attendance logs change.
2. **Subject-Scoped Biometric Queries**: Database queries for facial and vocal matching fetch *only* the students enrolled in the active subject, rather than the entire institutional database.
3. **Selective Column Queries**: General profile lookups and dashboard renders omit heavy 128-float and 256-float arrays, saving megabytes of bandwidth per request.
4. **Image Downsampling**: High-resolution 24MP–48MP smartphone photos are automatically scaled to max 1920px prior to face detection, reducing inference time from ~20s to <1.5s per image.
