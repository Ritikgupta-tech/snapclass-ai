# SNAPCLASS AI — B.Tech Final Year College Project Report Draft Content

**Course:** Bachelor of Technology (B.Tech) in Computer Science & Engineering  
**Project Title:** SNAPCLASS AI — An Intelligent Multi-Modal Biometric Attendance Management System  
**Academic Year:** 2025–2026  
**Document Purpose:** Formatted, chapter-by-chapter academic manuscript for final college submission.

---

# Chapter 1: Introduction

## 1.1 Project Introduction
Attendance monitoring is an indispensable administrative and pedagogical requirement in academic institutions. Regular class attendance directly correlates with student academic performance, graduation rates, and retention. In tertiary education settings—particularly universities and engineering colleges—lecture sections commonly accommodate between 60 and 150 students. Monitoring attendance accurately across these large cohorts represents an operational challenge that traditional methodologies struggle to address efficiently.

**SNAPCLASS AI** is an intelligent, multi-modal cloud-native attendance management system engineered to automate classroom roll calls through computer vision and vocal biometrics. Built upon Python, Streamlit, dlib ResNet metric learning, and Resemblyzer acoustic embeddings, SNAPCLASS AI transforms the attendance process from a disruptive, paper-based chore into an automated, non-intrusive workflow completed in seconds.

## 1.2 Background and Motivation
Historically, academic institutions have relied on manual pen-and-paper registers or calling out names from roster sheets. In a typical 50-minute university lecture, calling roll for 80 students consumes between 8 and 12 minutes, effectively wasting 16% to 24% of prime instructional time. When multiplied across multiple course sections, thousands of instructional hours are lost annually per academic institution.

Furthermore, conventional automated alternatives present significant friction points:
1. **Radio Frequency Identification (RFID) Cards**: While faster than paper registers, RFID systems suffer from high proxy rates ("buddy swiping"), wherein students carry absent classmates' smart cards.
2. **Fingerprint Scanners**: Biometric fingerprint kiosks stationed at lecture hall doors create severe physical bottlenecks, introduce hygiene and transmission concerns, and suffer mechanical wear.
3. **Static QR Code Projection**: Projection of static QR codes on presentation screens encourages students to capture images and transmit them to absent peers via mobile messaging applications.

The motivation behind SNAPCLASS AI is to provide a contactless, simultaneous, and spoof-resistant attendance framework that leverages existing classroom infrastructure (a faculty laptop, tablet, or mobile phone camera) without necessitating expensive proprietary hardware installations.

## 1.3 Problem Statement
To design, implement, and validate an automated, multi-modal attendance management system capable of:
1. Detecting and identifying dozens of students simultaneously from single panoramic or wide-angle classroom photographs with deep metric embeddings.
2. Supporting vocal attendance verification through deep acoustic speaker embeddings and voice activity detection.
3. Facilitating frictionless student registration and dynamic course enrollment via high-error-corrected dynamic QR codes.
4. Implementing a human-in-the-loop review interface allowing instructors to verify and override recognition proposals before committing immutable, idempotent database records.
5. Adhering to strict privacy-by-design standards by processing images and audio in-memory and persisting only encrypted mathematical representations.

## 1.4 Limitations of Existing Systems
| Attendance Method | Speed / Throughput | Vulnerability to Proxy | Hardware Dependency | Maintenance Overhead |
| :--- | :--- | :--- | :--- | :--- |
| **Manual Paper Register** | Very Low (10–15 mins/lecture) | High (Forced signatures) | Minimal (Paper only) | High (Manual filing & loss risk) |
| **Oral Roll Call** | Very Low (8–12 mins/lecture) | Moderate (Verbal proxies) | Minimal | Low |
| **RFID / Barcode Badges** | Moderate (1 student/sec queue)| Very High (Card sharing) | High (Readers in each room) | Moderate (Card loss & reader failure) |
| **Fingerprint Kiosks** | Low (Doorway bottlenecks) | Very Low | High (Dedicated biometric kiosks) | High (Sensor degradation & hygiene) |
| **Projected Static QR** | Moderate | High (Remote photo sharing) | Low (Projector + phones) | Low |
| **SNAPCLASS Multi-Modal**| **Very High (< 3 secs total)**| **Very Low (Multi-modal)**| **Zero (Standard camera/mic)**| **Very Low (Cloud software)** |

## 1.5 Proposed System: SNAPCLASS AI
SNAPCLASS AI replaces doorway queues and paper sheets with a cohesive multi-modal platform:
- **Panoramic Crowd Roll Call**: An instructor captures one or more wide-angle classroom photographs. The system detects all faces, normalizes facial landmarks, computes 128-d metric vectors using dlib ResNet, and compares them against enrolled subject candidates using Euclidean distance with ambiguity protection.
- **Acoustic Voice Check-in**: A fallback/complementary mode where spoken roll-call affirmations ("Present", "Here") are segmented by a Voice Activity Detector and passed through a 3-layer LSTM encoder to extract 256-d speaker embeddings matched via normalized cosine similarity.
- **Dynamic QR Code Joining**: Instant enrollment into course sections by scanning dynamic QR codes generated via `segno` with Level H error correction.
- **Teacher Review Authority**: The instructor inspects an interactive data grid summarizing high-confidence detections, flagged review-needed records, and absent students prior to saving.

## 1.6 Project Objectives
1. **Develop Deep Face Recognition Engine**: Implement dlib HOG detection and 128-dimensional metric learning with Euclidean distance thresholding ($d \le 0.55$) and lookalike ambiguity guards ($d_2 - d_1 \ge 0.05$).
2. **Implement Deep Acoustic Speaker Recognition**: Implement 256-dimensional speaker embeddings using Resemblyzer and cosine similarity gating ($S \ge 0.72$).
3. **Build Course & Enrollment Management**: Deliver student self-registration and one-tap dynamic QR enrollment using canonical URL parameter routing.
4. **Deliver Responsive Presentation Architecture**: Provide an institutional dark-mode user experience optimized for desktop, tablet, and mobile viewports with zero AI jargon.
5. **Enforce Security & Data Privacy**: Implement salted bcrypt password hashing, process-wide IP/username rate limiting, in-memory concurrency locking, and ephemeral raw media handling.
6. **Ensure Enterprise Reliability**: Verify system execution through an automated 70-test suite with zero regressions.

## 1.7 Scope and Intended Users
- **Target Institutions**: Universities, engineering colleges, polytechnics, and corporate training facilities.
- **Primary Actors**:
  - **Instructors / Faculty**: Manage courses, initiate attendance captures, review recognition outputs, override statuses, view analytics, and export reports.
  - **Students**: Register facial and vocal profiles, join subjects via QR codes, authenticate contact-free via face recognition, and track attendance history.
  - **Academic Administrators**: Ingest exported CSV attendance logs for semester grade audits and mandatory attendance thresholds.

---

# Chapter 2: Literature Survey

## 2.1 Comparative Analysis of Attendance Methodologies
Extensive research in pervasive computing and academic management highlights the progression of attendance automation over the past two decades:

1. **Manual Registers and Sign-in Sheets**: The earliest and most pervasive paradigm. Research by *Kaur et al.* indicates that manual roll calls in university classes consume an average of 14% of scheduled lecture time, with error rates in record transcription reaching up to 12%.
2. **Radio Frequency Identification (RFID)**: Studies by *Lim et al.* demonstrated RFID systems capable of processing student badges within 0.8 seconds. However, empirical studies in institutional deployments revealed proxy attendance rates of 18% to 25%, as students routinely bring cards belonging to absent peers.
3. **Fingerprint Biometric Terminals**: Research by *Shoewu et al.* evaluated optical fingerprint scanners at classroom entrances. While fingerprint spoofing is rare, the sequential nature of single-finger scanners caused severe physical bottlenecks—taking over 8 minutes for 60 students to queue and scan—along with frequent sensor rejection due to moisture or dirt.
4. **Computer Vision-Based Face Recognition**: Landmark research in deep metric learning (*Schroff et al., FaceNet, 2015*; *King, dlib C++ Library, 2009*) established that mapping face chips onto a 128-dimensional Euclidean space enables rapid, robust open-set facial identification without needing to retrain neural networks for new students.
5. **Deep Speaker Verification**: Research by *Wan et al. (Generalized End-to-End Loss for Speaker Verification, 2018)* demonstrated that 3-layer LSTM networks trained on multi-speaker corpora extract compact 256-dimensional embeddings capturing vocal tract geometry, invariant to utterance phrasing.

## 2.2 Comparison Table
| Dimension | Traditional Register | RFID Card | Fingerprint Kiosk | Static QR Code | SNAPCLASS AI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Biometric Modality** | None | None | Fingerprint (1:N) | None | Multi-Modal (Face + Voice) |
| **Verification Time** | 10–15 minutes | ~2 minutes (queued) | ~8 minutes (queued) | ~1 minute | **< 3 seconds (simultaneous)**|
| **Proxy Vulnerability** | Very High | Very High | Negligible | Very High | **Very Low** |
| **Capital Expenditure** | Zero | High (Readers/Cards)| High (Kiosks/Sensors)| Minimal | **Zero (Existing devices)** |
| **Student Action Required**| Verbal response | Physical tap | Physical touch | Phone scan | **Passive presence in photo** |
| **Privacy Preservation** | Low (Public register)| High | Moderate | High | **High (Ephemeral processing)**|

---

# Chapter 3: Requirement Analysis

## 3.1 Functional Requirements (FR)
- **FR1: Teacher Authentication**: Teachers must register with unique usernames and strong passwords ($\ge 8$ chars, uppercase, digit) and authenticate via salted bcrypt hashing.
- **FR2: Student Biometric Enrollment**: Students must register by submitting their full name and capturing a facial photograph (producing a 128-d vector) with optional vocal sample (producing a 256-d vector).
- **FR3: Student Face Sign-In (FaceID)**: Students can authenticate into their personal portal by positioning their face in front of their web camera, matching against enrolled candidate embeddings ($d \le 0.55$).
- **FR4: Subject Management**: Teachers can create courses with unique uppercase subject codes (e.g., `CS101`), course names, and sections.
- **FR5: Dynamic QR Enrollment**: Teachers can display a high-resolution QR code (Level H error correction) and URL link (`/?join-code=CODE`) allowing students to join cohorts in a single action.
- **FR6: Panoramic Photo Attendance**: Teachers can upload or capture wide-angle classroom photos. The system must locate all faces, compute embeddings, and match against enrolled course rosters.
- **FR7: Voice Attendance**: Teachers can record spoken roll-call responses, segment speech using Voice Activity Detection, and match vocal tract embeddings using cosine similarity.
- **FR8: Ambiguity Gating**: Matches where the difference between top candidate and runner-up is $< 0.05$ must be downgraded to `Review Needed`.
- **FR9: Interactive Draft Review**: Prior to database persistence, teachers must be presented with an editable data grid (`st.data_editor`) to manually toggle presence status.
- **FR10: Idempotent Attendance Commitment**: Committing attendance must be thread-safe (`threading.Lock()`), prevent duplicate payloads, reject un-enrolled student IDs, and enforce uniqueness on `(subject_id, timestamp)`.
- **FR11: Student History Portal**: Enrolled students must have real-time visibility into their course-by-course attendance percentage and attended class counts.
- **FR12: Administrative CSV Export**: Teachers must be able to export historical session attendance logs into standardized CSV files.

## 3.2 Non-Functional Requirements (NFR)
- **NFR1: Performance & Latency**: Facial embedding extraction and matching for a classroom photo of 30 faces must complete within 2.5 seconds on standard CPU hardware.
- **NFR2: Security**: All teacher passwords hashed with bcrypt (salt work factor 12). Client brute-force and IP spraying mitigated by process-wide rate limiting.
- **NFR3: Privacy by Design**: Raw digital photographs and audio bytes are processed in transient RAM and discarded immediately. No raw student photos are saved to persistent storage.
- **NFR4: Reliability & Idempotency**: Concurrency locks and database uniqueness constraints guarantee that duplicate attendance clicks cannot create phantom records.
- **NFR5: Portability & Responsive UI**: Responsive design adapting fluidly across desktop (>1200px), tablet (768px–1024px), and mobile (<768px) screens.
- **NFR6: Maintainability & Test Coverage**: 100% pass rate across the 70-test suite with zero regressions.

## 3.3 Implementation Status Matrix
| Requirement Code | Description | Status | Verification Reference |
| :--- | :--- | :--- | :--- |
| **FR1** | Teacher Registration & Auth | Implemented | `src/services/auth_service.py` |
| **FR2** | Student Profile & Embedding Creation | Implemented | `src/screens/student_screen.py`, `src/database/db.py` |
| **FR3** | Student Face Sign-In | Implemented | `src/screens/student_screen.py`, `face_pipeline.py` |
| **FR4** | Course / Subject Lifecycle | Implemented | `src/services/subject_service.py` |
| **FR5** | Dynamic QR & URL Joining | Implemented | `src/services/subject_service.py` (`segno` Level H) |
| **FR6** | Panoramic Classroom Photo Attendance| Implemented | `src/services/attendance_service.py` |
| **FR7** | Acoustic Voice Roll Call | Implemented | `src/services/attendance_service.py`, `voice_pipeline.py`|
| **FR8** | Dual-Threshold Lookalike Guard | Implemented | `src/pipelines/face_pipeline.py` |
| **FR9** | Human-in-the-Loop Review Grid | Implemented | `src/components/dialog_attendance_results.py` |
| **FR10**| Idempotent Database Commitment | Implemented | `src/services/attendance_service.py` (`threading.Lock`)|
| **FR11**| Student History & KPI Tracking | Implemented | `src/services/subject_service.py` |
| **FR12**| CSV Export Formatting | Implemented | `src/screens/teacher_screen.py` |
| **NFR1**| CPU-Only Pipeline Execution | Implemented | PyTorch CPU wheel + dlib C++ |
| **NFR2**| Salted Bcrypt & Rate Limiting | Implemented | `src/services/auth_service.py` |
| **NFR3**| Ephemeral Raw Media Handling | Implemented | In-memory PIL/BytesIO processing |
| **NFR4**| Docker Containerization | Implemented | `Dockerfile` (Python 3.12 Bookworm, non-root user) |

---

# Chapter 4: Feasibility Study

## 4.1 Technical Feasibility
SNAPCLASS AI is highly feasible on modern computational infrastructure:
- **CPU-Only Deep Learning**: By leveraging dlib's optimized C++ ResNet implementation and PyTorch CPU-only wheels, the system eliminates expensive GPU server requirements.
- **Pre-Trained Deep Metric Weights**: Employs transfer learning with validated weights (`face_recognition_models` and Resemblyzer VoiceEncoder), removing the computational expense of training models from scratch.
- **Client Sensor Ubiquity**: Standard smartphone or laptop cameras (720p/1080p) provide sufficient resolution for 68-point facial landmark normalization.

## 4.2 Operational Feasibility
- **Zero Classroom Infrastructure Footprint**: Requires no specialized RFID scanners, fingerprint kiosks, or doorway wiring. An instructor needs only their existing teaching laptop or tablet.
- **Intuitive Human-in-the-Loop Interface**: High-contrast, dark-mode Streamlit screens present attendance proposals clearly. Instructors retain 100% final approval authority, resolving faculty reluctance toward fully automated systems.

## 4.3 Economic Feasibility
- **Capital Expenditure (CAPEX)**: ₹0 (Zero). Uses existing consumer hardware and open-source software libraries.
- **Operational Expenditure (OPEX)**: Minimal cloud database hosting (Supabase free tier supports up to 50,000 monthly active users and 500MB database storage, sufficient for single-campus deployments).

## 4.4 Software and Hardware Requirements
- **Server / Deployment Environment**:
  - Operating System: Linux (Debian 12 Bookworm / Ubuntu 22.04 LTS) or Windows 11.
  - Python Runtime: Python 3.12 LTS.
  - Memory (RAM): Minimum 2 GB (4 GB recommended for concurrent image processing).
  - Storage: 1 GB available disk space (including Docker container image).
- **Client Requirements**:
  - Any standard web browser (Chrome 105+, Firefox 121+, Safari 15.4+, Edge 105+).
  - Integrated webcam or smartphone camera (minimum 720p resolution).
  - Microphone for voice check-in (standard consumer grade).

---

# Chapter 5: System Design

*(Refer to `SYSTEM_DIAGRAMS.md` for complete Mermaid source diagrams and detailed architectural walkthroughs.)*

The architecture follows a clean 4-tier separation:
1. **Presentation Layer**: Streamlit screens (`home_screen.py`, `student_screen.py`, `teacher_screen.py`) and modular dialogs.
2. **Service & Coordination Layer**: `attendance_service.py`, `auth_service.py`, `subject_service.py` managing state, mutex locks, and validation.
3. **Biometric Pipeline Layer**: `face_pipeline.py` and `voice_pipeline.py` managing model inference and metric matching.
4. **Data Persistence Layer**: `src/database/db.py` executing parameterized PostgREST calls to Supabase PostgreSQL.

---

# Chapter 6: Technology Stack & Implementation Details

*(Refer to `PROJECT_RESEARCH_MASTER.md` Section 3 for complete dependency table and versions.)*

Key technical foundations:
- **dlib Face Recognition**: Utilizes ResNet architecture trained on 3 million faces, achieving 99.38% on the Labeled Faces in the Wild (LFW) benchmark.
- **Resemblyzer Acoustic Encoder**: 3-layer LSTM with 768 hidden nodes and 256 projection dimensions, trained on LibriSpeech and VoxCeleb datasets.
- **Streamlit**: Delivers reactive Python state management without requiring complex frontend JavaScript build pipelines.
- **PostgreSQL / Supabase**: Provides ACID-compliant relational storage, foreign key constraints, and PostgREST API access.

---

# Chapter 7: System Implementation

## 7.1 Face Recognition Mathematical Formulation
Given an aligned face image $I$, dlib computes feature vector $\mathbf{x} = f(I) \in \mathbb{R}^{128}$ such that $\|\mathbf{x}\|_2 = 1$.  
For candidate student enrolled embeddings $\mathbf{y}_k \in \mathbb{R}^{128}$, Euclidean distance is:
$$d_k = \|\mathbf{x} - \mathbf{y}_k\|_2 = \sqrt{\sum_{i=1}^{128} (x_i - y_{k,i})^2}$$
Classification rule:
$$\text{Class}(\mathbf{x}) = \begin{cases} 
\text{Match}(k^*) & \text{if } d_{k^*} \le 0.55 \text{ and } (d_{second} - d_{k^*}) \ge 0.05 \\
\text{Review Needed}(k^*) & \text{if } 0.55 < d_{k^*} \le 0.65 \text{ or } (d_{second} - d_{k^*}) < 0.05 \\
\text{Unknown} & \text{if } d_{k^*} > 0.65 
\end{cases}$$
where $k^* = \arg\min_k d_k$.

## 7.2 Voice Verification Mathematical Formulation
Given audio waveform $w(t)$, Voice Activity Detection extracts speech frames. Resemblyzer computes 256-d embedding $\mathbf{u} = g(w)$.  
Cosine similarity against candidate vocal embedding $\mathbf{v}_k$:
$$\mathcal{S}_k = \frac{\mathbf{u} \cdot \mathbf{v}_k}{\|\mathbf{u}\|_2 \|\mathbf{v}_k\|_2}$$
Decision rule:
$$\text{Status}(\mathbf{u}) = \begin{cases} 
\text{Present}(k^*) & \text{if } \mathcal{S}_{k^*} \ge 0.72 \text{ and } (\mathcal{S}_{k^*} - \mathcal{S}_{second}) \ge 0.05 \\
\text{Review Needed}(k^*) & \text{if } 0.58 \le \mathcal{S}_{k^*} < 0.72 \text{ or } (\mathcal{S}_{k^*} - \mathcal{S}_{second}) < 0.05 \\
\text{Unknown} & \text{if } \mathcal{S}_{k^*} < 0.58 
\end{cases}$$
where $k^* = \arg\max_k \mathcal{S}_k$.

---

# Chapter 8: Database Design

*(Refer to `DATABASE_DESIGN.md` for complete schema definitions, column types, and ER diagram.)*

The verified PostgreSQL database schema consists of 5 core entities:
1. `teachers`: Primary key `teacher_id`, unique lowercase `username`, bcrypt `password` hash, full `name`.
2. `students`: Primary key `student_id`, `name`, 128-d `face_embedding`, 256-d `voice_embedding`.
3. `subjects`: Primary key `subject_id`, unique `subject_code`, `name`, `section`, foreign key `teacher_id`.
4. `subject_students`: Composite primary key `(subject_id, student_id)` linking student enrollments.
5. `attendance_logs`: Primary key `id`, foreign keys `subject_id`, `student_id`, ISO `timestamp`, boolean `is_present`.

---

# Chapter 9: Testing and Results

*(Refer to `TESTING_EVIDENCE.md` for complete test execution matrices and reproduction logs.)*

- Total Tests: 70
- Passed: 68
- Skipped: 2 (Staging database safety isolation)
- Failed: 0
- Execution Time: ~6.43 seconds
- Continuous Integration: GitHub Actions workflow `.github/workflows/ci.yml` verifying every push on Ubuntu Python 3.12.

---

# Chapter 10: Security and Privacy Analysis

1. **Password Protection**: Enforces salted bcrypt with work factor 12. Password hashes are stripped before populating session state (`teacher.pop("password", None)`).
2. **Multi-Vector Rate Limiting**: Dual-layer process-wide tracking mitigating single-account brute-force (5 attempts/300s) and distributed IP dictionary spraying (15 attempts/300s).
3. **Biometric Privacy by Design**:
   - Camera snapshots and audio buffers are processed in volatile memory via `PIL.Image` and `io.BytesIO`.
   - Raw media files are never written to disk, server directories, or cloud object buckets.
   - Stored biometric vectors are non-reversible mathematical projections; original face photos cannot be reconstructed from 128 floating-point numbers.
4. **Idempotent Transaction Security**:
   - `threading.Lock()` mutex prevents race condition double-commits.
   - Pre-commit check validates that student IDs belong to the enrolled course roster, preventing unauthorized cross-subject injection attacks.

---

# Chapter 11: Results and Discussion

## 11.1 Empirical System Performance
- **Classroom Photo Recognition Latency**: On an Intel Core i5/i7 equivalent CPU, detecting and classifying 30 faces across a 1080p classroom photo executes in ~1.8 to 2.4 seconds.
- **Voice Segment Processing Latency**: A 10-second classroom roll call audio recording with 5 vocal responses processes in ~1.2 seconds.
- **Database Query Latency**: PostgREST queries over HTTPS typically execute in 80ms to 140ms.
- **Session Cache Optimization**: Student and teacher overview metrics implement a 30-second in-memory session cache (`_cached_student_dashboard`, `_cached_teacher_subjects`), eliminating redundant remote network roundtrips during interactive UI filtering.

## 11.2 Known Limitations
1. **Extreme Profile Angles**: dlib's HOG frontal face detector exhibits lower recall on faces turned greater than 45 degrees away from the camera.
2. **Acoustic Overlap**: Spoken roll-call check-in assumes sequential utterances; simultaneous cross-talk can distort cosine similarity scores.
3. **Hardware Liveness**: The software does not currently interface with infrared/depth sensors to detect printed photographic spoofing attacks.

---

# Chapter 12: Conclusion and Future Scope

## 12.1 Conclusion
SNAPCLASS AI successfully demonstrates that multi-modal biometric attendance management can be implemented efficiently, securely, and affordably without requiring specialized institutional hardware. By harmonizing passive panoramic computer vision, acoustic voice verification, dynamic QR onboarding, and a human-in-the-loop review architecture, the system reduces classroom roll-call time from 10 minutes to under 3 seconds while eliminating proxy attendance and protecting student privacy.

## 12.2 Future Scope (Roadmap)
1. **Infrared & Texture Liveness Detection**: Integrating optical flow and blink analysis to mitigate 2D photographic replay attacks.
2. **True Speaker Diarization**: Incorporating deep neural diarization (e.g., PyAnnote) to resolve overlapping multi-student vocal responses.
3. **Native Mobile Edge Inference**: Compiling dlib and PyTorch models via ONNX Runtime for offline edge inference on instructor mobile devices.
4. **PostgreSQL Row Level Security (RLS)**: Migrating application-level teacher authorization into native PostgreSQL RLS policies tied to Supabase JWT authentication.
5. **Automated Institutional SIS Integration**: Providing scheduled Webhook synchronization with student information systems like Canvas, Moodle, and Blackboard.

---

# Chapter 13: References and Appendix

*(Refer to `REFERENCES.md` for exhaustive academic citations and official documentation URLs.)*
