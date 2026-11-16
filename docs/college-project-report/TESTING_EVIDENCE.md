# SNAPCLASS AI — Comprehensive Testing Evidence & Quality Assurance Report

**Course:** B.Tech Computer Science & Engineering  
**Project:** SNAPCLASS AI  
**Test Framework:** Pytest 9.2.0 (`pytest.ini`, `tests/conftest.py`)  
**Execution Environment:** Python 3.14.6 (Local) / Python 3.12 LTS (GitHub Actions Ubuntu Runner)  
**Report Date:** November 2026  
**Test Execution Summary:** 70 Tests Collected | 68 Passed | 2 Skipped (Staging Safety Gate) | 0 Failed  

---

## 1. Quality Assurance Strategy & Test Pyramid

The quality assurance strategy for SNAPCLASS AI is structured according to the classic test pyramid:
1. **Unit Tests (50 Tests)**: Fast, isolated verification of mathematical distance functions, threshold logic, input sanitizers, image normalizers, audio payload headers, and bcrypt cryptographic functions.
2. **Integration Tests (12 Tests)**: Multi-component coordination testing between service layers, database abstraction mock adapters, idempotency locks, and transaction aggregators.
3. **Workflow & Regression Tests (8 Tests)**: End-to-end simulation of the complete attendance lifecycle (from teacher registration to CSV export) and regression verification for previously fixed edge-case bugs.

```text
               /\
              /  \
             / E2E\        --> 8 Workflow & Regression Tests (End-to-End Lifecycle)
            /------\
           / Integr \      --> 12 Service & Database Integration Tests
          /----------\
         /    Unit    \    --> 50 Low-Level Algorithmic, Validation & Security Tests
        /--------------\
```

---

## 2. Test Execution Baseline Reproduction Log

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\DELL\Desktop\SNAPCLASS\venv\scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\DELL\Desktop\SNAPCLASS
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.16.0, platformdirs-4.14.5
collecting ... collected 70 items

tests/integration/test_attendance_service.py::TestAttendanceService::test_idempotent_confirmation PASSED [  1%]
tests/integration/test_attendance_service.py::TestAttendanceService::test_db_level_duplicate_timestamp_rejected PASSED [  2%]
tests/integration/test_attendance_service.py::TestAttendanceService::test_unauthorized_teacher_rejected PASSED [  4%]
tests/integration/test_attendance_service.py::TestAttendanceService::test_get_teacher_attendance_overview_grouping PASSED [  5%]
tests/integration/test_attendance_service.py::TestAttendanceService::test_duplicate_student_records_in_payload_deduplicated PASSED [  7%]
tests/integration/test_attendance_service.py::TestAttendanceService::test_unregistered_student_in_attendance_rejected PASSED [  8%]
tests/integration/test_attendance_service.py::TestAttendanceService::test_db_unique_constraint_violation_handled_gracefully PASSED [ 10%]
tests/integration/test_real_db_workflow.py::TestRealDatabaseStagingWorkflow::test_real_supabase_connectivity SKIPPED [ 11%]
tests/integration/test_real_db_workflow.py::TestRealDatabaseStagingWorkflow::test_real_database_idempotent_session_insert SKIPPED [ 12%]
tests/integration/test_subject_service.py::TestSubjectService::test_generate_qr_share_details PASSED [ 14%]
tests/integration/test_subject_service.py::TestSubjectService::test_create_new_subject_duplicate_code_rejected PASSED [ 15%]
tests/integration/test_subject_service.py::TestSubjectService::test_get_student_dashboard_data_aggregations PASSED [ 17%]
tests/unit/test_face_pipeline.py::TestFacePipeline::test_exact_face_match PASSED [ 18%]
tests/unit/test_face_pipeline.py::TestFacePipeline::test_ambiguous_face_match PASSED [ 20%]
tests/unit/test_face_pipeline.py::TestFacePipeline::test_unknown_face PASSED [ 21%]
tests/unit/test_face_pipeline.py::TestFacePipeline::test_empty_candidates_returns_unknown PASSED [ 22%]
tests/unit/test_face_pipeline.py::TestFacePipeline::test_corrupt_candidate_vector_handled_gracefully PASSED [ 24%]
tests/unit/test_face_pipeline.py::TestFacePipeline::test_multiple_candidates_picks_closest PASSED [ 25%]
tests/unit/test_face_pipeline.py::TestFacePipeline::test_scoped_candidate_isolation PASSED [ 27%]
tests/unit/test_face_pipeline.py::TestFacePipeline::test_similar_candidates_downgraded_to_needs_review PASSED [ 28%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_bcrypt_hashing_and_verification PASSED [ 30%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_rate_limiting_lockout_after_max_attempts PASSED [ 31%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_rate_limiting_persists_across_streamlit_session_restarts PASSED [ 32%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_register_teacher_rejects_weak_passwords PASSED [ 34%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_register_teacher_rejects_mismatched_passwords PASSED [ 35%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_logout_purges_authenticated_state PASSED [ 37%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_rate_limiting_composite_ip_spraying_lockout PASSED [ 38%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_missing_credentials_handled_gracefully PASSED [ 40%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_cross_subject_unauthorized_teacher_injection PASSED [ 41%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_teacher_cannot_access_other_teacher_subjects PASSED [ 42%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_teacher_cannot_access_other_teacher_attendance_records PASSED [ 44%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_students_cannot_submit_attendance_for_other_students PASSED [ 45%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_raw_embeddings_and_passwords_never_exposed_in_session_state PASSED [ 47%]
tests/unit/test_security_auth.py::TestSecurityAndAuth::test_invalid_or_expired_authentication_rejected PASSED [ 48%]
tests/unit/test_validators.py::TestInputValidators::test_validate_username_valid PASSED [ 50%]
tests/unit/test_validators.py::TestInputValidators::test_validate_username_invalid_chars PASSED [ 51%]
tests/unit/test_validators.py::TestInputValidators::test_validate_username_too_short PASSED [ 52%]
tests/unit/test_validators.py::TestInputValidators::test_validate_username_empty PASSED [ 54%]
tests/unit/test_validators.py::TestInputValidators::test_validate_password_strong PASSED [ 55%]
tests/unit/test_validators.py::TestInputValidators::test_validate_password_too_short PASSED [ 57%]
tests/unit/test_validators.py::TestInputValidators::test_validate_password_missing_number PASSED [ 58%]
tests/unit/test_validators.py::TestInputValidators::test_validate_password_missing_uppercase PASSED [ 60%]
tests/unit/test_validators.py::TestInputValidators::test_validate_subject_inputs_valid PASSED [ 61%]
tests/unit/test_validators.py::TestInputValidators::test_validate_subject_inputs_missing_code PASSED [ 62%]
tests/unit/test_validators.py::TestInputValidators::test_validate_subject_inputs_invalid_code PASSED [ 64%]
tests/unit/test_validators.py::TestInputValidators::test_sanitize_string PASSED [ 65%]
tests/unit/test_validators.py::TestAudioValidators::test_empty_audio_payload PASSED [ 67%]
tests/unit/test_validators.py::TestAudioValidators::test_none_audio_payload PASSED [ 68%]
tests/unit/test_validators.py::TestAudioValidators::test_oversized_audio_payload PASSED [ 70%]
tests/unit/test_validators.py::TestImageValidators::test_none_image PASSED [ 71%]
tests/unit/test_validators.py::TestImageValidators::test_tiny_image PASSED [ 72%]
tests/unit/test_validators.py::TestImageValidators::test_valid_image PASSED [ 74%]
tests/unit/test_validators.py::TestImageValidators::test_oversized_image_downscaled PASSED [ 75%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_cosine_similarity_properties PASSED [ 77%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_identify_speaker_high_confidence PASSED [ 78%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_identify_speaker_ambiguous_threshold PASSED [ 80%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_identify_speaker_unknown PASSED [ 81%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_process_bulk_audio_empty_bytes PASSED [ 82%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_process_bulk_audio_none_bytes PASSED [ 84%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_identify_speaker_skips_invalid_embeddings PASSED [ 85%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_identify_speaker_picks_best_match_among_candidates PASSED [ 87%]
tests/unit/test_voice_pipeline.py::TestVoicePipeline::test_similar_voice_speakers_downgraded_to_needs_review PASSED [ 88%]
tests/workflows/test_e2e_attendance_flow.py::TestEndToEndAttendanceFlow::test_complete_attendance_lifecycle PASSED [ 90%]
tests/workflows/test_regression_bugs.py::TestRegressionFixes::test_voice_attendance_none_audio_does_not_crash PASSED [ 91%]
tests/workflows/test_regression_bugs.py::TestRegressionFixes::test_voice_recognition_failure_does_not_mark_all_students_absent PASSED [ 92%]
tests/workflows/test_regression_bugs.py::TestRegressionFixes::test_face_pipeline_single_student_no_svc_crash PASSED [ 94%]
tests/workflows/test_regression_bugs.py::TestRegressionFixes::test_canonical_app_url_has_valid_https_scheme PASSED [ 95%]
tests/workflows/test_regression_bugs.py::TestRegressionFixes::test_subject_card_closure_safety PASSED [ 97%]
tests/workflows/test_regression_bugs.py::TestRegressionFixes::test_voice_session_zero_matches_halts_gracefully PASSED [ 98%]
tests/workflows/test_regression_bugs.py::TestRegressionFixes::test_csv_export_structure PASSED [100%]

======================== 68 passed, 2 skipped in 6.43s ========================
```

---

## 3. Comprehensive Test Case Matrix (70 Items)

### 3.1 Integration Test Suite: Attendance Service (`tests/integration/test_attendance_service.py`)

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **INT-ATT-01** | `test_idempotent_confirmation` | Double submission of same `session_id` within mutex lock returns error | Blocked with duplicate message on 2nd attempt | **PASSED** |
| **INT-ATT-02** | `test_db_level_duplicate_timestamp_rejected` | Submitting session when timestamp exists in DB returns error | Database check rejects insert | **PASSED** |
| **INT-ATT-03** | `test_unauthorized_teacher_rejected` | Teacher attempting to save attendance for unowned subject is rejected | Unauthorized error returned | **PASSED** |
| **INT-ATT-04** | `test_get_teacher_attendance_overview_grouping` | Raw flat attendance rows correctly grouped by distinct `(timestamp, subject_id)` | Grouped into session dicts with counts | **PASSED** |
| **INT-ATT-05** | `test_duplicate_student_records_in_payload_deduplicated`| Payload containing duplicate student IDs pre-filtered before insert | Exactly 1 record per student sent to DB | **PASSED** |
| **INT-ATT-06** | `test_unregistered_student_in_attendance_rejected` | Submitting student ID not on enrolled roster aborts commit | Rejection error indicating non-enrolled ID | **PASSED** |
| **INT-ATT-07** | `test_db_unique_constraint_violation_handled_gracefully`| DB unique constraint violation (`23505`) caught and mapped to user message | Clean failure message, no unhandled exception | **PASSED** |

---

### 3.2 Integration Test Suite: Real Database Staging (`tests/integration/test_real_db_workflow.py`)

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **INT-RDB-01** | `test_real_supabase_connectivity` | Live connection to dedicated staging DB | Skipped when staging flags absent | **SKIPPED (Guarded)**|
| **INT-RDB-02** | `test_real_database_idempotent_session_insert` | Full lifecycle synthetic CRUD on staging DB | Skipped when staging flags absent | **SKIPPED (Guarded)**|

> **Staging Safety Guard**: These tests execute only when `SNAPCLASS_STAGING_TEST_RUN=true` and `SNAPCLASS_ENV=staging`. They protect the live Supabase production database from receiving synthetic or test rows during automated CI and developer testing.

---

### 3.3 Integration Test Suite: Subject Service (`tests/integration/test_subject_service.py`)

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **INT-SUB-01** | `test_generate_qr_share_details` | High-res QR code PNG bytes and canonical URL generated | Output contains valid PNG bytes and `?join-code=` | **PASSED** |
| **INT-SUB-02** | `test_create_new_subject_duplicate_code_rejected` | Creating subject with existing uppercase code is rejected | Rejection message returned | **PASSED** |
| **INT-SUB-03** | `test_get_student_dashboard_data_aggregations` | Student attendance logs grouped by subject with percentage | Summary math matches classes attended/total | **PASSED** |

---

### 3.4 Unit Test Suite: Face Recognition Pipeline (`tests/unit/test_face_pipeline.py`)

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **UNT-FCE-01** | `test_exact_face_match` | Euclidean distance $\le 0.55$ classifies as `HIGH_CONFIDENCE` | Matched with status `HIGH_CONFIDENCE` | **PASSED** |
| **UNT-FCE-02** | `test_ambiguous_face_match` | Distance between $0.55$ and $0.65$ classifies as `NEEDS_REVIEW` | Status `NEEDS_REVIEW` | **PASSED** |
| **UNT-FCE-03** | `test_unknown_face` | Distance $> 0.65$ classifies as `UNKNOWN` | Returns `None, None, dist, "UNKNOWN"` | **PASSED** |
| **UNT-FCE-04** | `test_empty_candidates_returns_unknown` | Empty enrolled candidate list returns `UNKNOWN` safely | Status `UNKNOWN` without exception | **PASSED** |
| **UNT-FCE-05** | `test_corrupt_candidate_vector_handled_gracefully` | Candidate vector with invalid shape ($\ne 128$) skipped | Skipped gracefully; returns `UNKNOWN` | **PASSED** |
| **UNT-FCE-06** | `test_multiple_candidates_picks_closest` | Chooses candidate with smallest Euclidean norm | Identifies closest candidate | **PASSED** |
| **UNT-FCE-07** | `test_scoped_candidate_isolation` | Only candidates from active subject roster are matched | External candidates completely ignored | **PASSED** |
| **UNT-FCE-08** | `test_similar_candidates_downgraded_to_needs_review` | Runner-up distance gap $< 0.05$ triggers lookalike downgrade | Status downgraded to `NEEDS_REVIEW` | **PASSED** |

---

### 3.5 Unit Test Suite: Security & Authentication (`tests/unit/test_security_auth.py`)

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **UNT-SEC-01** | `test_bcrypt_hashing_and_verification` | Passwords hashed with salt; verifiable via `check_pass` | Bcrypt hashes match plaintext | **PASSED** |
| **UNT-SEC-02** | `test_rate_limiting_lockout_after_max_attempts` | 5 failed logins triggers temporary lockout | 6th attempt locked out with remaining seconds | **PASSED** |
| **UNT-SEC-03** | `test_rate_limiting_persists_across_streamlit_session_restarts` | Module-level mutex persists lockout even if UI re-runs | Lockout persists across session re-evaluations | **PASSED** |
| **UNT-SEC-04** | `test_register_teacher_rejects_weak_passwords` | Password missing uppercase or number rejected | Registration rejected with policy error | **PASSED** |
| **UNT-SEC-05** | `test_register_teacher_rejects_mismatched_passwords` | Mismatched password and confirm password rejected | Rejection error returned | **PASSED** |
| **UNT-SEC-06** | `test_logout_purges_authenticated_state` | Calling logout removes `teacher_data`, `student_data` | Session state keys completely cleared | **PASSED** |
| **UNT-SEC-07** | `test_rate_limiting_composite_ip_spraying_lockout` | 15 failed logins from single IP locks out IP address | IP-level lockout triggered | **PASSED** |
| **UNT-SEC-08** | `test_missing_credentials_handled_gracefully` | Empty username or password handled without crash | Rejection message returned | **PASSED** |
| **UNT-SEC-09** | `test_cross_subject_unauthorized_teacher_injection` | Teacher cannot save attendance for subject they do not own | Unauthorized rejection returned | **PASSED** |
| **UNT-SEC-10** | `test_teacher_cannot_access_other_teacher_subjects` | Querying subjects filters strictly by `teacher_id` | Foreign subjects omitted from result | **PASSED** |
| **UNT-SEC-11** | `test_teacher_cannot_access_other_teacher_attendance_records`| Querying logs filters strictly by teacher's subjects | Foreign logs omitted from result | **PASSED** |
| **UNT-SEC-12** | `test_students_cannot_submit_attendance_for_other_students` | Attendance review requires teacher authorization | Student role blocked from confirmation | **PASSED** |
| **UNT-SEC-13** | `test_raw_embeddings_and_passwords_never_exposed_in_session_state`| Passwords and vectors stripped from returned dicts | Sensitive fields popped before return | **PASSED** |
| **UNT-SEC-14** | `test_invalid_or_expired_authentication_rejected` | Stale or unauthenticated session access redirected | Protected screens block execution | **PASSED** |

---

### 3.6 Unit Test Suite: Input & Media Validators (`tests/unit/test_validators.py`)

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **UNT-VAL-01** | `test_validate_username_valid` | Alphanumeric lowercase username accepted | `(True, "")` | **PASSED** |
| **UNT-VAL-02** | `test_validate_username_invalid_chars` | Special characters (e.g. `@`, `$`) in username rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-03** | `test_validate_username_too_short` | Username $< 3$ characters rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-04** | `test_validate_username_empty` | Empty username rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-05** | `test_validate_password_strong` | Complex password ($\ge 8$ chars, upper, number) accepted | `(True, "")` | **PASSED** |
| **UNT-VAL-06** | `test_validate_password_too_short` | Password $< 8$ characters rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-07** | `test_validate_password_missing_number` | Password without digits rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-08** | `test_validate_password_missing_uppercase`| Password without uppercase letters rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-09** | `test_validate_subject_inputs_valid` | Valid code, title, and section accepted | `(True, "")` | **PASSED** |
| **UNT-VAL-10** | `test_validate_subject_inputs_missing_code`| Missing subject code rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-11** | `test_validate_subject_inputs_invalid_code`| Code with spaces or symbols rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-12** | `test_sanitize_string` | Strips control characters and leading/trailing whitespace | Cleaned string | **PASSED** |
| **UNT-VAL-13** | `test_empty_audio_payload` | Zero-byte audio buffer rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-14** | `test_none_audio_payload` | None audio input rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-15** | `test_oversized_audio_payload` | Audio $> 10\text{ MB}$ rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-16** | `test_none_image` | None image input rejected | `(False, "...")` | **PASSED** |
| **UNT-VAL-17** | `test_tiny_image` | Image $< 50\text{px}$ rejected as insufficient resolution | `(False, "...")` | **PASSED** |
| **UNT-VAL-18** | `test_valid_image` | Standard RGB image accepted | `(True, "", np_arr)` | **PASSED** |
| **UNT-VAL-19** | `test_oversized_image_downscaled` | Image $> 1920\text{px}$ downscaled preserving aspect ratio | Width/height $\le 1920\text{px}$ | **PASSED** |

---

### 3.7 Unit Test Suite: Voice Recognition Pipeline (`tests/unit/test_voice_pipeline.py`)

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **UNT-VOC-01** | `test_cosine_similarity_properties` | Normalized dot product yields $\cos(\theta) \in [-1, 1]$ | Correct scalar | **PASSED** |
| **UNT-VOC-02** | `test_identify_speaker_high_confidence` | Cosine similarity $\ge 0.72$ classifies as `HIGH_CONFIDENCE` | Status `HIGH_CONFIDENCE` | **PASSED** |
| **UNT-VOC-03** | `test_identify_speaker_ambiguous_threshold`| Score between $0.58$ and $0.72$ classifies as `NEEDS_REVIEW` | Status `NEEDS_REVIEW` | **PASSED** |
| **UNT-VOC-04** | `test_identify_speaker_unknown` | Score $< 0.58$ classifies as `UNKNOWN` | Status `UNKNOWN` | **PASSED** |
| **UNT-VOC-05** | `test_process_bulk_audio_empty_bytes` | Empty audio buffer halts gracefully with error message | Error returned, no crash | **PASSED** |
| **UNT-VOC-06** | `test_process_bulk_audio_none_bytes` | None audio buffer halts gracefully | Error returned, no crash | **PASSED** |
| **UNT-VOC-07** | `test_identify_speaker_skips_invalid_embeddings` | Candidate vector with invalid dimension ($\ne 256$) skipped | Skips corrupt vectors safely | **PASSED** |
| **UNT-VOC-08** | `test_identify_speaker_picks_best_match_among_candidates`| Chooses candidate with maximum cosine similarity | Selects top candidate | **PASSED** |
| **UNT-VOC-09** | `test_similar_voice_speakers_downgraded_to_needs_review`| Score gap to runner-up $< 0.05$ downgrades to `NEEDS_REVIEW`| Status downgraded to `NEEDS_REVIEW` | **PASSED** |

---

### 3.8 Workflow & Regression Test Suite (`tests/workflows/`)

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **WFK-E2E-01** | `test_complete_attendance_lifecycle` | End-to-end flow: register teacher $\rightarrow$ create course $\rightarrow$ enroll student $\rightarrow$ photo attendance $\rightarrow$ confirm $\rightarrow$ student history | Complete lifecycle passes with consistent state | **PASSED** |
| **REG-FIX-01** | `test_voice_attendance_none_audio_does_not_crash` | None audio passed to voice attendance handler does not raise Unhandled Exception | Handled gracefully with warning | **PASSED** |
| **REG-FIX-02** | `test_voice_recognition_failure_does_not_mark_all_students_absent`| Low-confidence audio recording preserves review status rather than blindly marking all absent | Correct review flags set | **PASSED** |
| **REG-FIX-03** | `test_face_pipeline_single_student_no_svc_crash`| Classroom with exactly 1 enrolled student does not crash classification engine | Matches single candidate properly | **PASSED** |
| **REG-FIX-04** | `test_canonical_app_url_has_valid_https_scheme` | `CANONICAL_APP_URL` guaranteed to possess valid HTTPS scheme without trailing slash | Valid HTTPS URL | **PASSED** |
| **REG-FIX-05** | `test_subject_card_closure_safety` | Unenroll button callback closure safely binds `subject_id` avoiding loop variable capture | Unique key and correct subject targeted | **PASSED** |
| **REG-FIX-06** | `test_voice_session_zero_matches_halts_gracefully`| Audio recording with zero recognizable voices returns actionable message | User warned, zero unhandled errors | **PASSED** |
| **REG-FIX-07** | `test_csv_export_structure` | Exported CSV contains standard columns: `Timestamp, Subject, Section, Student Name, Status` | Matches expected schema | **PASSED** |
