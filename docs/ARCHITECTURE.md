# SNAPCLASS AI — System Architecture Specification

**Document Version**: 2.3.0  
**Target Environment**: Streamlit SaaS (Option B) / Python 3.12 LTS Docker & Python 3.14 / Supabase PostgreSQL 15  
**Architectural Decision**: Retain and upgrade Streamlit architecture with modular service, validation, and pipeline layers.

---

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph ClientLayer [Presentation & Interaction Layer]
        Router[app.py Global Router]
        HomeScreen[src/screens/home_screen.py]
        TeacherScreen[src/screens/teacher_screen.py]
        StudentScreen[src/screens/student_screen.py]
        Dialogs[src/components/ Dialog Suite]
        Theme[src/ui/base_layout.py & .streamlit/config.toml]
    end

    subgraph ServiceLayer [Business Logic & Service Layer]
        AuthService[src/services/auth_service.py]
        SubjectService[src/services/subject_service.py]
        AttendanceService[src/services/attendance_service.py]
    end

    subgraph BiometricLayer [Biometric Recognition Pipelines]
        FacePipeline[src/pipelines/face_pipeline.py]
        VoicePipeline[src/pipelines/voice_pipeline.py]
        Validators[src/validators/ - Image, Audio, Input]
    end

    subgraph DataLayer [Data Persistence & Configuration Layer]
        DBAccess[src/database/db.py]
        Config[src/database/config.py]
        Supabase[(Supabase PostgreSQL 15)]
    end

    Router --> HomeScreen
    Router --> TeacherScreen
    Router --> StudentScreen
    TeacherScreen --> Dialogs
    StudentScreen --> Dialogs

    TeacherScreen --> SubjectService
    TeacherScreen --> AttendanceService
    StudentScreen --> AuthService
    StudentScreen --> SubjectService

    AttendanceService --> FacePipeline
    AttendanceService --> VoicePipeline
    AttendanceService --> DBAccess
    AuthService --> DBAccess
    SubjectService --> DBAccess

    FacePipeline --> Validators
    VoicePipeline --> Validators

    DBAccess --> Config
    Config --> Supabase
```

---

## 2. Docker & Containerization Architecture

SNAPCLASS AI includes a multi-platform, production-ready `Dockerfile` targeting **Python 3.12 LTS on Debian Bookworm Slim**:

- **Base Image**: `python:3.12-slim-bookworm`
- **System Dependencies**: `build-essential`, `cmake`, `git`, `curl`, `libopenblas-dev`, `liblapack-dev`, `libx11-dev`, `libgtk-3-dev`, `libsndfile1`, `ffmpeg`.
- **Security**: Runs under an unprivileged non-root user (`appuser`, UID 1001).
- **Health Monitoring**: Integrated `HEALTHCHECK` querying Streamlit core probe:
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
      CMD curl --fail http://localhost:8501/_stcore/health || exit 1
  ```
- **Configuration Flexibility**: `src/database/config.py` resolves credentials first from standard OS environment variables (`SUPABASE_URL`, `SUPABASE_KEY`, `SNAPCLASS_ENV`) and falls back to `.streamlit/secrets.toml`.

---

## 3. Layer Responsibilities & Module Directory Structure

```text
SNAPCLASS/
├── Dockerfile                       # Multi-platform Python 3.12 container specification
├── .dockerignore                    # Excludes secrets, git history, and caches
├── app.py                           # Application entrypoint & query-param router
├── requirements.txt                 # Pinned dependencies
├── .streamlit/
│   ├── config.toml                  # Premium dark/light palette theme configuration
│   └── secrets.toml.example         # Template for Supabase credentials & environment flags
├── docs/                            # Architectural, security, migration & QA documentation
├── src/
│   ├── config/
│   │   └── app_config.py            # Global thresholds, durations, limits, and URLs
│   ├── database/
│   │   ├── config.py                # Dual environment variable / secrets credential resolver
│   │   └── db.py                    # Data access layer, safe queries & password hashing
│   ├── services/
│   │   ├── auth_service.py          # Authentication, password rules & composite rate limiting
│   │   ├── subject_service.py       # Subject creation, roster management, QR generation
│   │   └── attendance_service.py    # Multi-modal review drafting, mutex locking & confirmation
│   ├── pipelines/
│   │   ├── face_pipeline.py         # 128-d dlib face embeddings, Euclidean matching, twin guards
│   │   └── voice_pipeline.py        # 256-d Resemblyzer embeddings, cosine matching, close-speaker guards
│   ├── validators/
│   │   ├── input_validators.py      # Username, password, code sanitization & validation
│   │   ├── image_validators.py      # PIL image format, resolution and scaling checks
│   │   └── audio_validators.py      # Audio duration, size, and header validation
│   ├── screens/
│   │   ├── home_screen.py           # Landing page with hero section & portal selection
│   │   ├── teacher_screen.py        # Instructor workspace, tabs, subject cards, session history
│   │   └── student_screen.py        # Student portal, FaceID login, courses, attendance history
│   ├── components/
│   │   ├── header.py & footer.py    # Consistent navigation headers and footers
│   │   ├── subject_card.py          # Polished academic card component
│   │   └── dialog_*.py              # Modal dialogs for creation, photos, voice & review
│   └── ui/
│       └── base_layout.py           # Typography, container width rules & transition styles
└── tests/                           # 65-test automated test suite
    ├── unit/                        # Face, voice, auth, security & validator tests
    ├── integration/                 # Attendance and subject service integration tests
    │   └── test_real_db_workflow.py # Explicit real DB tests (skipped without staging env)
    └── workflows/                   # Full 14-step E2E lifecycle and regression tests
```
