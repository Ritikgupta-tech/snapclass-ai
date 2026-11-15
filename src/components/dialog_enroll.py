"""
Dialog for students to manually join a subject using a subject code.
"""

import streamlit as st
import time
from src.services.subject_service import enroll_student_by_code

@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.caption("Enter the unique subject code shared by your instructor to join the course roster.")

    student_data = st.session_state.get("student_data")
    if not student_data or "student_id" not in student_data:
        st.error("You must be logged in as a student to enroll in subjects.")
        if st.button("Close", key="dlg_enroll_unauth_close"):
            st.rerun()
        return

    student_id = student_data["student_id"]
    join_code = st.text_input("Subject Code *", placeholder="e.g. CS101", key="dlg_manual_join_code")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", width="stretch", key="dlg_enroll_cancel"):
            st.rerun()

    with col2:
        if st.button("Join Subject", type="primary", width="stretch", key="dlg_enroll_submit"):
            if not join_code:
                st.warning("Please enter a subject code.")
            else:
                success, msg, sub = enroll_student_by_code(student_id, join_code)
                if success:
                    st.success(msg)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(msg)
