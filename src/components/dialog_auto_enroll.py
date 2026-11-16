"""
Dialog for automatic QR link enrollment when a student opens an invite link.
"""

import streamlit as st
import time
from src.database.db import (
    get_subject_by_code,
    get_student_subjects
)
from src.services.subject_service import enroll_student_by_code

@st.dialog("Course Invitation")
def auto_enroll_dialog(subject_code: str):
    clean_code = (subject_code or "").strip().upper()
    student_data = st.session_state.get("student_data")

    if not student_data or "student_id" not in student_data:
        st.info("Please log in with your Student FaceID to join this course.")
        if st.button("Close", key="auto_enroll_unauth_close"):
            st.query_params.clear()
            st.rerun()
        return

    student_id = student_data["student_id"]
    subject = get_subject_by_code(clean_code)

    if not subject:
        st.error(f"Invalid invitation: No subject found with code '{clean_code}'.")
        if st.button("Dismiss", key="auto_enroll_notfound_btn"):
            st.query_params.clear()
            st.rerun()
        return

    # Check if already enrolled
    enrolled_nodes = get_student_subjects(student_id)
    enrolled_ids = [n["subject_id"] for n in enrolled_nodes if n.get("subject_id")]

    if subject["subject_id"] in enrolled_ids:
        st.info(f"You are already enrolled in **{subject['name']}** ({clean_code})!")
        if st.button("Go to Dashboard", type="primary", key="auto_enroll_already_btn"):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"""
    You have been invited to join:
    - **Subject**: {subject['name']}
    - **Code**: `{clean_code}`
    - **Section**: {subject.get('section', 'General')}
    """)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Decline", width="stretch", key="auto_enroll_decline_btn"):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button("Accept & Join Class", type="primary", width="stretch", key="auto_enroll_accept_btn"):
            success, msg, _ = enroll_student_by_code(student_id, clean_code)
            if success:
                st.session_state.pop("_cached_student_dashboard", None)
                st.session_state.pop("_cached_teacher_subjects", None)
                st.success(f"Enrolled successfully in {subject['name']}!")
                st.query_params.clear()
                time.sleep(1.2)
                st.rerun()
            else:
                st.error(msg)
