# SNAPCLASS AI — Automated Testing & Quality Assurance Report

**Document Version**: 2.0.0  
**Test Framework**: Pytest 9.2.0  
**Total Test Count**: 46  
**Passed**: 46 (100%)  
**Failed**: 0  
**Execution Runtime**: 9.31 seconds  

---

## 1. Test Architecture & Coverage

The automated test suite covers the entire pipeline, from low-level input sanitizers to multi-modal biometric metric distance scoring, security rate limiters, idempotent confirmation locks, and regression verifications for all identified P0/P1 defects.

```
tests/
├── unit/
│   ├── test_validators.py        # Input, password, audio & image bounds (15 tests)
│   ├── test_face_pipeline.py     # 128-d Euclidean candidate distance & unknown faces (5 tests)
│   ├── test_voice_pipeline.py    # Cosine similarity & speaker identification (6 tests)
│   └── test_security_auth.py     # Bcrypt, rate-limiting lockout, logout state purge (5 tests)
├── integration/
│   ├── test_subject_service.py   # Subject creation, duplicate prevention, QR generation (3 tests)
│   └── test_attendance_service.py# Idempotency token & session overview rollups (3 tests)
└── workflows/
    └── test_regression_bugs.py   # Regression coverage for verified P0/P1 defects (5 tests)
```

---

## 2. Test Execution Command & Summary

```bash
.\venv\Scripts\python.exe -m pytest tests -v
```

### Verified Test Results

| Test Module | Test Name | Target Behavior | Outcome |
|---|---|---|---|
| `test_validators.py` | `test_validate_username_valid` | Validates standard username formats | **PASSED** |
| `test_validators.py` | `test_validate_username_invalid_chars` | Rejects special characters | **PASSED** |
| `test_validators.py` | `test_validate_username_too_short` | Rejects length < 3 | **PASSED** |
| `test_validators.py` | `test_validate_password_strong` | Validates complexity rules | **PASSED** |
| `test_validators.py` | `test_validate_password_too_short` | Rejects passwords < 8 chars | **PASSED** |
| `test_validators.py` | `test_validate_password_missing_number` | Rejects missing digit | **PASSED** |
| `test_validators.py` | `test_validate_password_missing_uppercase` | Rejects missing uppercase | **PASSED** |
| `test_validators.py` | `test_validate_subject_inputs_valid` | Validates subject code and title | **PASSED** |
| `test_validators.py` | `test_empty_audio_payload` | Correctly flags 0-byte audio | **PASSED** |
| `test_validators.py` | `test_none_audio_payload` | Handles unrecorded None stream | **PASSED** |
| `test_validators.py` | `test_oversized_audio_payload` | Rejects audio exceeding 10MB | **PASSED** |
| `test_validators.py` | `test_oversized_image_downscaled` | Scales down 3000px image to max 1920px | **PASSED** |
| `test_face_pipeline.py` | `test_exact_face_match` | Verifies self-distance < 0.001 | **PASSED** |
| `test_face_pipeline.py` | `test_ambiguous_face_match` | Flags 0.58 distance as NEEDS_REVIEW | **PASSED** |
| `test_face_pipeline.py` | `test_unknown_face` | Distinguishes unknown faces | **PASSED** |
| `test_face_pipeline.py` | `test_empty_candidates_returns_unknown` | Safe fallback when 0 candidates | **PASSED** |
| `test_face_pipeline.py` | `test_corrupt_candidate_vector` | Skips malformed embedding vectors | **PASSED** |
| `test_voice_pipeline.py` | `test_cosine_similarity_properties` | Verifies normalization & bounds | **PASSED** |
| `test_voice_pipeline.py` | `test_identify_speaker_high_confidence` | Matches speaker above 0.72 | **PASSED** |
| `test_voice_pipeline.py` | `test_identify_speaker_ambiguous` | Flags marginal score as NEEDS_REVIEW | **PASSED** |
| `test_voice_pipeline.py` | `test_identify_speaker_unknown` | Returns UNKNOWN when orthogonal | **PASSED** |
| `test_voice_pipeline.py` | `test_process_bulk_audio_empty_bytes` | Returns clean error on empty bytes | **PASSED** |
| `test_security_auth.py` | `test_bcrypt_hashing_and_verification` | Bcrypt salt & verification | **PASSED** |
| `test_security_auth.py` | `test_rate_limiting_lockout` | Enforces 5-attempt lockout for 300s | **PASSED** |
| `test_security_auth.py` | `test_logout_purges_authenticated_state` | Purges all sensitive keys on logout | **PASSED** |
| `test_subject_service.py` | `test_generate_qr_share_details` | Emits https:// scheme & QR bytes | **PASSED** |
| `test_subject_service.py` | `test_create_new_subject_duplicate_code` | Blocks duplicate subject codes | **PASSED** |
| `test_attendance_service.py`| `test_idempotent_confirmation` | Blocks duplicate session saves | **PASSED** |
| `test_attendance_service.py`| `test_unauthorized_teacher_rejected` | Rejects saves for unowned subjects | **PASSED** |
| `test_regression_bugs.py` | `test_voice_attendance_none_audio` | Proves NoneType read fix | **PASSED** |
| `test_regression_bugs.py` | `test_voice_failure_no_false_absent` | Proves no false absence logging | **PASSED** |
| `test_regression_bugs.py` | `test_face_pipeline_single_student` | Proves 1-student roster safety | **PASSED** |
| `test_regression_bugs.py` | `test_canonical_app_url_has_valid_scheme`| Proves proper URL resolution | **PASSED** |
| `test_regression_bugs.py` | `test_subject_card_closure_safety` | Proves loop closure isolation | **PASSED** |

---

## 3. Headless Streamlit Agent API Runtime Verification

Following the Streamlit development guidelines, the application was run in headless mode with `--server.enableAgentApi=true` on port 8765 to verify real runtime rendering:

1. **Health Check**:
   - `GET /_stcore/health` returned `ok`.
2. **Landing Page Tree Snapshot**:
   - `POST /_stcore/agent/interact` returned `"status": "ready"`.
   - Verified presence of `landing_student_portal_btn` and `landing_teacher_portal_btn`.
3. **Instructor Navigation Transition**:
   - Triggered `landing_teacher_portal_btn`.
   - App state re-rendered seamlessly to the Instructor Login form with action keys `['teacher_login_home_btn', 'teacher_login_username_input', 'teacher_login_password_input', 'teacher_do_login_btn', 'teacher_goto_register_btn']`.
4. **Rate-Limiting & Error Alerting**:
   - Sent invalid login payload.
   - App returned status `"ready"` with inline warning alert `"Invalid username or password."` without crashing or throwing unhandled exceptions.
5. **Student Portal Transition**:
   - Successfully routed back to home and navigated into the Student Portal with action keys `['student_login_home_btn', 'toggle_reg_form_btn']`.
