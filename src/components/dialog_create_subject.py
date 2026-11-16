"""
Dialog for creating new academic course subjects.
"""

import streamlit as st
from src.services.subject_service import create_new_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id: int):
    st.caption("Define the course identifier, name, and batch/section for this subject.")

    sub_code = st.text_input("Subject Code *", placeholder="e.g. CS101 or MATH202", key="dlg_create_sub_code")
    sub_name = st.text_input("Subject Name *", placeholder="e.g. Data Structures & Algorithms", key="dlg_create_sub_name")
    sub_section = st.text_input("Section / Batch *", placeholder="e.g. Section A, Batch 2026", key="dlg_create_sub_sec")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", width="stretch", key="dlg_create_sub_cancel"):
            st.rerun()

    with col2:
        if st.button("Create Subject", type="primary", width="stretch", key="dlg_create_sub_submit"):
            success, msg, subject_data = create_new_subject(teacher_id, sub_code, sub_name, sub_section)
            if success:
                st.session_state.pop("_cached_teacher_subjects", None)
                st.toast(msg, icon="✅")
                st.session_state["subject_created_toast"] = msg
                st.rerun()
            else:
                st.error(msg)
