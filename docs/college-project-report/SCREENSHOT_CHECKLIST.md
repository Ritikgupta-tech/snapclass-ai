# SNAPCLASS AI — Comprehensive Screenshot Checklist & Visual Evidence Guide

**Course:** B.Tech Computer Science & Engineering  
**Project:** SNAPCLASS AI  
**Document Purpose:** Actionable screenshot capture catalog for B.Tech thesis and presentation slides.  
**Execution Environment:** Application running locally at `http://localhost:8501` or on Streamlit Cloud at `https://snapclass-ai-attendence-system.streamlit.app`.  

---

## 1. Visual Capture Standards & Guidelines

For academic thesis submission, all screenshots must adhere to the following standards:
1. **Aspect Ratio & Resolution**:
   - Primary Desktop View: Minimum $1920 \times 1080$ px (Full HD) at 100% browser scaling.
   - Mobile View: $375 \times 812$ px (iPhone viewport) or $412 \times 915$ px (Android viewport).
   - Format: Lossless PNG format (`.png`) to preserve high-contrast font crispness.
2. **Color Palette Consistency**: Ensure the browser renders in dark mode (`#070A10` background) without third-party extension color overrides.
3. **Data Anonymization**: Use realistic academic sample data (e.g., `Dr. Ananya Roy`, `Ritik Gupta`, `CS101`, `Data Structures & Algorithms`) rather than placeholder gibberish (`asdf`, `test1`).

---

## 2. Master Screenshot Catalog (12 Required Figures)

| Fig. # | Screen Title | Academic Report Placement | Navigation Route / Trigger Action | Visual Contents to Capture | Capture Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fig. 1** | **Public Landing Portal & Live Status** | Chapter 1 (Introduction) & Chapter 7 (Implementation) | Root URL `/` (Unauthenticated state) | - Top luxury header with "SNAPCLASS PRO EDITION"<br>- Live Telemetry Bar ("SYSTEM HEALTH: 100% OPERATIONAL")<br>- Hero Title: "Classroom Attendance, Perfectly Automated."<br>- Four Performance Pillars (Speed, Accuracy, Privacy, Records)<br>- Role entrypoint cards (Student Portal vs Instructor Workspace) | **Ready to Capture** |
| **Fig. 2** | **Instructor Sign-In & Registration Modal** | Chapter 3 (Requirements) & Chapter 7 (Implementation) | Click "Enter Instructor Workspace" $\rightarrow$ Toggle "Create Account" | - Dark card container with "Instructor Login" header<br>- Form fields: Username, Password, Name<br>- Primary button "Sign In" with icon `:material/login:`<br>- Tertiary button "Create Account"<br>- Clean validation hints | **Ready to Capture** |
| **Fig. 3** | **Instructor Workspace & KPI Dashboard** | Chapter 5 (Design) & Chapter 7 (Implementation) | Log in as instructor $\rightarrow$ Main view | - Faculty Session Badge with instructor name & handle<br>- Action buttons ("Refresh", "Sign Out") in top toolbar<br>- Three overview KPI metrics: Total Subjects, Enrolled Students, Attendance Sessions<br>- Primary navigation buttons: "Take Attendance", "Manage Subjects", "Attendance Records" | **Ready to Capture** |
| **Fig. 4** | **Course / Subject Management Interface** | Chapter 3 (Requirements) & Chapter 7 (Implementation) | Instructor Dashboard $\rightarrow$ Click "Manage Subjects" tab | - Section subheader "Your Managed Academic Subjects"<br>- Action button "+ Create New Subject"<br>- Dialog modal with inputs: Subject Code (e.g., `CS101`), Subject Name, Section<br>- Grid of created subject cards displaying code badges and enroll counts | **Ready to Capture** |
| **Fig. 5** | **Dynamic Subject QR Code & Join Link** | Chapter 3 (Requirements) & Chapter 7 (Implementation) | Click "Share QR Code" on any Subject Card | - Dialog modal titled "Enroll in [Subject Name]"<br>- Crisp, high-resolution Level H QR code PNG image<br>- One-tap direct join URL (`/?join-code=CODE`)<br>- Formatted instruction for classroom projector display | **Ready to Capture** |
| **Fig. 6** | **Student Camera Face Sign-In (FaceID)** | Chapter 3 (Requirements) & Chapter 7 (Implementation) | Landing Page $\rightarrow$ Click "Enter Student Portal" | - Camera viewfinder box with live video feed<br>- Status badge: "CAMERA READY"<br>- Instruction caption: "Center your face in the camera view"<br>- Capture trigger button for instant recognition sign-in | **Ready to Capture** |
| **Fig. 7** | **Student Authenticated Dashboard & Courses** | Chapter 5 (Design) & Chapter 7 (Implementation) | Authenticate as student $\rightarrow$ Dashboard view | - Student metadata header with ID number & "VERIFIED PROFILE" badge<br>- Overview metrics: Enrolled Courses, Total Classes, Attended, Overall Attendance %<br>- Enrolled course cards (`dsa`, `cs`) with green progress indicators<br>- Secondary action button "Unenroll from Course" | **Ready to Capture** |
| **Fig. 8** | **Panoramic Photo Upload & Crowd Roll Call** | Chapter 7 (Implementation) & Chapter 9 (Testing) | Instructor Dashboard $\rightarrow$ "Take Attendance" $\rightarrow$ "Panoramic Classroom Photo" | - Camera / File uploader for multi-image classroom capture<br>- Image preview showing lecture hall crowd<br>- Real-time processing spinner: "Analyzing classroom faces..."<br>- Summary metric showing detected student count vs unknown faces | **Ready to Capture** |
| **Fig. 9** | **Acoustic Voice-Activated Attendance View**| Chapter 7 (Implementation) & Chapter 9 (Testing) | Instructor Dashboard $\rightarrow$ "Take Attendance" $\rightarrow$ "Voice Attendance (Spoken Roll Call)" | - Audio recorder widget with recording waveform indicator<br>- Instructions for spoken roll call<br>- Processing feedback spinner: "Processing audio..."<br>- Acoustic similarity match counter | **Ready to Capture** |
| **Fig. 10**| **Interactive Attendance Review Data Grid** | Chapter 7 (Implementation) & Chapter 10 (Security) | Photo or Audio processing completes $\rightarrow$ Results dialog | - Interactive `st.data_editor` table<br>- Columns: Student Name, Present? (Checkbox), Detected Status, Confidence %, Source<br>- Editable presence toggles for instructor manual override<br>- Final tally caption: "X Present, Y Absent"<br>- Action buttons: "Confirm & Save Attendance" vs "Cancel" | **Ready to Capture** |
| **Fig. 11**| **Historical Attendance Records Log & Details** | Chapter 7 (Implementation) & Chapter 11 (Results) | Instructor Dashboard $\rightarrow$ Click "Attendance Records" tab | - Subject filter dropdown (`All Subjects` vs individual courses)<br>- Historical session card list with timestamp & attendance rate badge<br>- Expandable section: "View Student Roster Detail"<br>- Breakdown table of student-by-student presence for selected date | **Ready to Capture** |
| **Fig. 12**| **CSV Export & Edge-Case Validation States** | Chapter 7 (Implementation) & Chapter 9 (Testing) | Instructor Records view $\rightarrow$ Click "Export CSV" / Validation triggers | - CSV download button with icon `:material/download:`<br>- Notification toasts: "Attendance confirmed!", "Already recorded in database"<br>- Input validation alerts: "Password must contain at least 8 characters...", "Subject code already exists" | **Ready to Capture** |

---

## 3. Recommended Academic Figure Captions

- **Figure 1**: *SNAPCLASS AI Public Portal showing institutional branding, live operational telemetry, performance metrics, and dual role entrypoints.*
- **Figure 2**: *Faculty Authentication modal featuring salted bcrypt credential validation and client rate-limiting controls.*
- **Figure 3**: *Instructor Workspace Dashboard presenting aggregated cohort metrics and primary operational tabs.*
- **Figure 4**: *Course Creation interface with strict uppercase subject code uniqueness enforcement and section assignment.*
- **Figure 5**: *Dynamic QR Code modal generated via `segno` with Level H error correction and direct URL join routing.*
- **Figure 6**: *Student Portal contact-free Face Sign-In (FaceID) interface utilizing client webcam feed.*
- **Figure 7**: *Student Dashboard displaying enrolled academic subjects, attendance percentage KPIs, and session tallies.*
- **Figure 8**: *Panoramic classroom photo analysis detecting multi-student faces simultaneously across lecture rows.*
- **Figure 9**: *Voice-activated attendance capture analyzing classroom speech frames via Voice Activity Detection.*
- **Figure 10**: *Human-in-the-Loop attendance review data grid (`st.data_editor`) allowing manual faculty overrides prior to commitment.*
- **Figure 11**: *Historical attendance session log with drill-down roster expansion and aggregate attendance rates.*
- **Figure 12**: *Administrative CSV export generation and graceful exception handling for duplicate session submissions.*
