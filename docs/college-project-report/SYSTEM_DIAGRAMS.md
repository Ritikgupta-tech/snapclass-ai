# SNAPCLASS AI — Comprehensive System Diagrams & Technical Schematics

**Course:** B.Tech Computer Science & Engineering  
**Project:** SNAPCLASS AI  
**Document Purpose:** Complete Mermaid diagrams and academic walkthroughs for report insertion.

---

## 1. Overall System Architecture Diagram

This diagram illustrates the 4-tier layered architecture of SNAPCLASS AI, showing the boundaries between presentation, service coordination, biometric inference, and cloud persistence.

```mermaid
flowchart TD
    subgraph PresentationTier ["Presentation Tier (Streamlit Reactive UI)"]
        Router["app.py (Route Dispatcher)"]
        HomeScreen["src/screens/home_screen.py (Public Portal)"]
        TeacherScreen["src/screens/teacher_screen.py (Faculty Workspace)"]
        StudentScreen["src/screens/student_screen.py (Student Dashboard)"]
        Dialogs["src/components/ Dialog & Modal Suite"]
        UIEngine["src/ui/base_layout.py (CSS Layout Engine)"]
    end

    subgraph ServiceTier ["Service & Coordination Tier (Business Logic)"]
        AuthService["src/services/auth_service.py (Authentication & Rate Limiting)"]
        SubjectService["src/services/subject_service.py (Course Lifecycle & QR)"]
        AttendanceService["src/services/attendance_service.py (Session Mutex & Logic)"]
        Validators["src/validators/ (Input, Image, Audio Boundary Guards)"]
    end

    subgraph BiometricTier ["Biometric & AI Pipeline Tier (Inference Engine)"]
        FacePipeline["src/pipelines/face_pipeline.py (dlib ResNet 128-d Metric)"]
        VoicePipeline["src/pipelines/voice_pipeline.py (Resemblyzer 256-d LSTM)"]
        DlibModels["dlib Pretrained Weights (HOG + ResNet)"]
        VoiceEncoder["Resemblyzer VoiceEncoder (Pretrained LSTM)"]
    end

    subgraph PersistenceTier ["Data Persistence Tier (Cloud Database)"]
        DBAccess["src/database/db.py (PostgREST Query Layer)"]
        DBConfig["src/database/config.py (Environment Resolver)"]
        SupabaseDB[("Supabase PostgreSQL 15 Cloud Database")]
    end

    Router --> HomeScreen
    Router --> TeacherScreen
    Router --> StudentScreen
    TeacherScreen --> Dialogs
    StudentScreen --> Dialogs
    UIEngine -.-> PresentationTier

    TeacherScreen --> SubjectService
    TeacherScreen --> AttendanceService
    StudentScreen --> AuthService
    StudentScreen --> SubjectService

    AuthService --> Validators
    SubjectService --> Validators
    AttendanceService --> Validators

    AttendanceService --> FacePipeline
    AttendanceService --> VoicePipeline
    FacePipeline --> DlibModels
    VoicePipeline --> VoiceEncoder

    AuthService --> DBAccess
    SubjectService --> DBAccess
    AttendanceService --> DBAccess
    DBAccess --> DBConfig
    DBConfig --> SupabaseDB
```

---

## 2. Use Case Diagram

This diagram depicts the primary actors (Instructor and Student) and their interactions with the SNAPCLASS AI system boundaries.

```mermaid
flowchart LR
    Instructor["Instructor (Faculty)"]
    Student["Student (Learner)"]

    subgraph SNAPCLASS_System ["SNAPCLASS AI Boundary"]
        UC1["Register / Log In Account"]
        UC2["Create Course Subject"]
        UC3["Generate Subject QR Code"]
        UC4["Enroll in Subject via QR / Code"]
        UC5["Capture Classroom Panoramic Photo"]
        UC6["Execute Facial Recognition"]
        UC7["Record Vocal Roll Call"]
        UC8["Execute Acoustic Speaker Match"]
        UC9["Review & Override Attendance Draft"]
        UC10["Confirm & Commit Attendance Log"]
        UC11["View Attendance History & Percentages"]
        UC12["Export Session Attendance to CSV"]
        UC13["Student Face Sign-In (FaceID)"]
        UC14["Register Student Biometric Profile"]
    end

    Instructor --> UC1
    Instructor --> UC2
    Instructor --> UC3
    Instructor --> UC5
    Instructor --> UC6
    Instructor --> UC7
    Instructor --> UC8
    Instructor --> UC9
    Instructor --> UC10
    Instructor --> UC11
    Instructor --> UC12

    Student --> UC13
    Student --> UC14
    Student --> UC4
    Student --> UC11
```

---

## 3. Data Flow Diagram (DFD) — Level 0 (Context Level)

The Level 0 Context Diagram shows external entities exchanging raw information with the unified SNAPCLASS AI application boundary.

```mermaid
flowchart TD
    Instructor["Instructor (Teacher)"]
    Student["Student"]
    Database[("Supabase Cloud Database (PostgreSQL)")]

    subgraph SNAPCLASS_Context ["SNAPCLASS AI Attendance System (Level 0)"]
        SystemProcess["Central Attendance Processing System"]
    end

    Instructor -- "1. Credentials, Course Details, Classroom Photos, Audio Streams" --> SystemProcess
    SystemProcess -- "2. Recognition Proposals, Review Grids, Attendance Logs, CSV Summaries" --> Instructor

    Student -- "3. Registration Info, Face Image, Voice Sample, Join Code" --> SystemProcess
    SystemProcess -- "4. Authentication Status, Enrollment Confirmation, Attendance Metrics" --> Student

    SystemProcess -- "5. Parameterized SQL/PostgREST Queries, Log Inserts" --> Database
    Database -- "6. Stored Records, Enrolled Rosters, Biometric Embeddings" --> SystemProcess
```

---

## 4. Data Flow Diagram (DFD) — Level 1 (Decomposition)

The Level 1 DFD decomposes the central system into distinct sub-processes: Authentication, Course & QR Management, Biometric Processing, Review & Commitment, and History Analytics.

```mermaid
flowchart TD
    subgraph Processes ["SNAPCLASS AI Sub-Processes"]
        P1["1.0 Authentication & Rate Limiting"]
        P2["2.0 Course & QR Code Management"]
        P3["3.0 Multi-Modal Biometric Inference"]
        P4["4.0 Interactive Review & Idempotent Commit"]
        P5["5.0 History & Analytics Generation"]
    end

    subgraph DataStores ["Data Stores"]
        DS1[("D1: Teachers")]
        DS2[("D2: Students & Embeddings")]
        DS3[("D3: Subjects & Rosters")]
        DS4[("D4: Attendance Logs")]
    end

    Instructor["Instructor"]
    Student["Student"]

    Instructor -- "Teacher Credentials" --> P1
    P1 -- "Validate & Store Bcrypt Hash" --> DS1
    P1 -- "Auth Session Token" --> Instructor

    Student -- "Face Capture / Biometrics" --> P1
    P1 -- "Store Vectors" --> DS2
    P1 -- "Student Session Profile" --> Student

    Instructor -- "Course Info" --> P2
    P2 -- "Create Subject & QR" --> DS3
    Student -- "Scan QR / Submit Code" --> P2
    P2 -- "Enroll Link" --> DS3

    Instructor -- "Classroom Photo / Audio" --> P3
    DS2 -- "Enrolled Biometric Embeddings" --> P3
    DS3 -- "Course Candidate Filter" --> P3
    P3 -- "Raw Match Proposals" --> P4

    Instructor -- "Manual Overrides & Approval" --> P4
    P4 -- "Validated Attendance Logs" --> DS4

    DS4 -- "Historical Records" --> P5
    DS3 -- "Subject Metadata" --> P5
    P5 -- "Attendance Rate & Analytics" --> Student
    P5 -- "Aggregate History & CSV Export" --> Instructor
```

---

## 5. Entity-Relationship (ER) Diagram (Relational Database)

This diagram details the relational schema in Supabase PostgreSQL, showing primary keys, foreign keys, cardinality, and data attributes.

```mermaid
erDiagram
    TEACHERS ||--o{ SUBJECTS : "teaches and owns"
    SUBJECTS ||--o{ SUBJECT_STUDENTS : "enrolled in"
    STUDENTS ||--o{ SUBJECT_STUDENTS : "participates in"
    SUBJECTS ||--o{ ATTENDANCE_LOGS : "recorded for"
    STUDENTS ||--o{ ATTENDANCE_LOGS : "marked for"

    TEACHERS {
        bigint teacher_id PK "Auto-increment primary key"
        text username UK "Unique lowercase username"
        text password "Salted bcrypt hash (60 chars)"
        text name "Full legal name"
    }

    STUDENTS {
        bigint student_id PK "Auto-increment primary key"
        text name "Student full name"
        json face_embedding "128-d dlib float vector"
        json voice_embedding "256-d Resemblyzer float vector"
    }

    SUBJECTS {
        bigint subject_id PK "Auto-increment primary key"
        text subject_code UK "Unique uppercase code (e.g. CS101)"
        text name "Course subject title"
        text section "Classroom cohort / section"
        bigint teacher_id FK "References TEACHERS(teacher_id)"
    }

    SUBJECT_STUDENTS {
        bigint subject_id PK,FK "References SUBJECTS(subject_id)"
        bigint student_id PK,FK "References STUDENTS(student_id)"
    }

    ATTENDANCE_LOGS {
        bigint id PK "Auto-increment primary key"
        bigint subject_id FK "References SUBJECTS(subject_id)"
        bigint student_id FK "References STUDENTS(student_id)"
        text timestamp "ISO-8601 session timestamp"
        boolean is_present "True = Present, False = Absent"
    }
```

---

## 6. Activity Diagram — Classroom Attendance Workflow

This diagram models the dynamic operational steps taken by an instructor to conduct a biometric roll call using classroom photography.

```mermaid
flowchart TD
    Start([Instructor Launches Attendance Session]) --> SelectSubject[Select Subject from Dashboard]
    SelectSubject --> ChooseMode{Choose Biometric Mode}

    ChooseMode -- "Panoramic Photo" --> UploadPhoto[Capture / Upload Classroom Photo]
    ChooseMode -- "Audio Roll Call" --> RecordAudio[Record Classroom Audio Response]

    UploadPhoto --> ValidateImg[Validate Dimension <= 1920px & RGB Format]
    ValidateImg --> DetectFaces[Detect Faces via HOG & 68 Landmarks]
    DetectFaces --> ExtractFaceEmbeddings[Compute 128-d ResNet Embeddings]
    ExtractFaceEmbeddings --> ScopeCandidatesFace[Fetch Enrolled Roster Candidates]
    ScopeCandidatesFace --> CalcEuclidean[Calculate Euclidean Distances to Enrolled Vectors]
    CalcEuclidean --> ApplyFaceGating{Distance <= 0.55?}

    ApplyFaceGating -- Yes --> CheckFaceAmbiguity{Distance Gap to Runner-Up >= 0.05?}
    CheckFaceAmbiguity -- Yes --> MarkHighFace[Tag as HIGH_CONFIDENCE Present]
    CheckFaceAmbiguity -- No --> MarkReviewFace[Tag as NEEDS_REVIEW Flagged]
    ApplyFaceGating -- No --> CheckAmbiguousDist{Distance <= 0.65?}
    CheckAmbiguousDist -- Yes --> MarkReviewFace
    CheckAmbiguousDist -- No --> MarkUnknownFace[Tag as UNKNOWN]

    RecordAudio --> ValidateAudio[Validate Duration 0.5s-60s & Size <= 10MB]
    ValidateAudio --> SegmentSpeech[VAD Silence Segmentation via librosa]
    SegmentSpeech --> ExtractVoiceEmbeddings[Compute 256-d LSTM Embeddings]
    ExtractVoiceEmbeddings --> ScopeCandidatesVoice[Fetch Enrolled Roster Candidates]
    ScopeCandidatesVoice --> CalcCosine[Calculate Cosine Similarity to Enrolled Vectors]
    CalcCosine --> ApplyVoiceGating{Cosine Similarity >= 0.72?}

    ApplyVoiceGating -- Yes --> CheckVoiceAmbiguity{Score Gap to Runner-Up >= 0.05?}
    CheckVoiceAmbiguity -- Yes --> MarkHighVoice[Tag as HIGH_CONFIDENCE Present]
    CheckVoiceAmbiguity -- No --> MarkReviewVoice[Tag as NEEDS_REVIEW Flagged]
    ApplyVoiceGating -- No --> CheckAmbiguousScore{Score >= 0.58?}
    CheckAmbiguousScore -- Yes --> MarkReviewVoice
    CheckAmbiguousScore -- No --> MarkUnknownVoice[Tag as UNKNOWN]

    MarkHighFace --> CompileDraft[Compile Full Roster Attendance Draft]
    MarkReviewFace --> CompileDraft
    MarkUnknownFace --> CompileDraft
    MarkHighVoice --> CompileDraft
    MarkReviewVoice --> CompileDraft
    MarkUnknownVoice --> CompileDraft

    CompileDraft --> DisplayEditor[Display Interactive st.data_editor Grid]
    DisplayEditor --> FacultyReview{Instructor Overrides Needed?}
    FacultyReview -- Yes --> ManualToggle[Teacher Toggles Student Presence]
    FacultyReview -- No --> ConfirmClick[Teacher Clicks Confirm & Save]
    ManualToggle --> ConfirmClick

    ConfirmClick --> MutexLock[Acquire Process Concurrency Mutex Lock]
    MutexLock --> IdempotencyCheck{Session Already Saved in DB?}
    IdempotencyCheck -- Yes --> RejectDuplicate[Abort: Duplicate Session Prevented]
    IdempotencyCheck -- No --> DeduplicatePayload[Deduplicate Payload by Student ID]
    DeduplicatePayload --> VerifyRoster[Verify All IDs Belong to Enrolled Roster]
    VerifyRoster --> CommitDB[Execute Atomic Batch Insert in attendance_logs]
    CommitDB --> SuccessToast[Display Success Notification & Refresh Cache]
    RejectDuplicate --> End([Session Complete])
    SuccessToast --> End
```

---

## 7. Sequence Diagram — End-to-End Attendance Confirmation

This sequence diagram depicts runtime message passing between actors, UI controllers, background services, biometric inference pipelines, and the cloud PostgreSQL database.

```mermaid
sequenceDiagram
    autonumber
    actor Teacher as Instructor
    participant UI as teacher_screen.py
    participant Dialog as dialog_attendance_results.py
    participant Service as attendance_service.py
    participant Pipeline as face_pipeline.py
    participant DB as db.py
    participant Supabase as Supabase PostgreSQL

    Teacher->>UI: Selects Course & Uploads Classroom Photo
    UI->>Service: prepare_face_attendance_session(subject_id, images, teacher_id)
    Service->>DB: check_teacher_owns_subject(teacher_id, subject_id)
    DB->>Supabase: SELECT subject_id WHERE teacher_id = ...
    Supabase-->>DB: Verified Ownership
    Service->>DB: get_enrolled_students_for_subject(subject_id, include_embeddings=True)
    DB->>Supabase: SELECT subject_students JOIN students
    Supabase-->>DB: Returns Enrolled Student List with Vectors
    
    Service->>Pipeline: analyze_classroom_photo(image_np, enrolled_candidates)
    Pipeline->>Pipeline: dlib Detect Faces & Compute 128-d Vectors
    Pipeline->>Pipeline: Compute Euclidean Norm & Apply Dual Gating
    Pipeline-->>Service: Return Matches {student_id, distance, status}
    
    Service->>Service: Construct session_draft payload with DataFrame
    Service-->>UI: Return session_draft
    UI->>Dialog: Render dialog_attendance_results(session_draft)
    Dialog-->>Teacher: Displays Editable Table with Match Confidences

    Teacher->>Dialog: Manually adjusts student status & clicks "Confirm & Save"
    Dialog->>Service: confirm_and_save_attendance(teacher_id, session_id, subject_id, records)
    
    Service->>Service: Acquire _CONFIRM_LOCK (threading.Lock)
    Service->>DB: check_attendance_session_exists(subject_id, timestamp)
    DB->>Supabase: SELECT id FROM attendance_logs WHERE timestamp = ...
    Supabase-->>DB: Record Not Found (Idempotent OK)
    
    Service->>Service: Deduplicate student records in payload
    Service->>DB: create_attendance(deduped_records)
    DB->>Supabase: INSERT INTO attendance_logs VALUES (...)
    Supabase-->>DB: Insert Success Confirmation (N rows)
    Service->>Service: Release _CONFIRM_LOCK
    Service-->>Dialog: Return Success Message
    Dialog-->>Teacher: Displays Success Toast & Refreshes Dashboard View
```

---

## 8. Multi-Modal Recognition Decision Pipeline Architecture

This diagram details the twin metric evaluation engines for facial distance and vocal cosine similarity, showcasing how ambiguous samples are safely quarantined for human review.

```mermaid
flowchart TD
    InputMedia[Classroom Media Capture] --> RouteModality{Sensor Type}

    subgraph FaceEngine ["Facial Biometric Pipeline"]
        RouteModality -- "Visual Image" --> ImageNorm[Image Validation & Lanczos Downscaling]
        ImageNorm --> HOGDetect[HOG Linear SVM Frontal Face Detection]
        HOGDetect --> Align68[68-Point Landmark Facial Alignment]
        Align68 --> ResNet128[ResNet Forward Pass -> 128-d Unit Vector]
        ResNet128 --> NormDiff[Euclidean Metric d = ||x - y||_2]
        NormDiff --> FaceCond1{d <= 0.55?}
        FaceCond1 -- Yes --> FaceGap{Runner-Up Gap (d2 - d1) >= 0.05?}
        FaceGap -- Yes --> FaceHigh["HIGH_CONFIDENCE (Marked Present)"]
        FaceGap -- No --> FaceReview["NEEDS_REVIEW (Lookalike Guard)"]
        FaceCond1 -- No --> FaceCond2{d <= 0.65?}
        FaceCond2 -- Yes --> FaceReview
        FaceCond2 -- No --> FaceUnknown["UNKNOWN (Unidentified Face)"]
    end

    subgraph VoiceEngine ["Voice Biometric Pipeline"]
        RouteModality -- "Acoustic Audio" --> AudioNorm[Audio Validation & 16kHz Resampling]
        AudioNorm --> VADSplit[VAD Split on Non-Silent Frames top_db=25]
        VADSplit --> FilterNoise[Filter Transient Noise < 0.4s]
        FilterNoise --> LSTM256[3-Layer LSTM Forward Pass -> 256-d Unit Vector]
        LSTM256 --> CosineDot[Cosine Similarity S = (u . v) / (||u|| ||v||)]
        CosineDot --> VoiceCond1{S >= 0.72?}
        VoiceCond1 -- Yes --> VoiceGap{Runner-Up Gap (s1 - s2) >= 0.05?}
        VoiceGap -- Yes --> VoiceHigh["HIGH_CONFIDENCE (Marked Present)"]
        VoiceGap -- No --> VoiceReview["NEEDS_REVIEW (Acoustic Ambiguity Guard)"]
        VoiceCond1 -- No --> VoiceCond2{S >= 0.58?}
        VoiceCond2 -- Yes --> VoiceReview
        VoiceCond2 -- No --> VoiceUnknown["UNKNOWN (Unidentified Speaker)"]
    end

    FaceHigh --> ConsensusMerge[Human-in-the-Loop Review Consolidation]
    FaceReview --> ConsensusMerge
    FaceUnknown --> ConsensusMerge
    VoiceHigh --> ConsensusMerge
    VoiceReview --> ConsensusMerge
    VoiceUnknown --> ConsensusMerge

    ConsensusMerge --> InteractiveTable[Interactive Teacher Review Grid]
```
