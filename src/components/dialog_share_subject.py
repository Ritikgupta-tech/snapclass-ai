"""
Dialog for sharing subject codes and join QR codes.
"""

import streamlit as st
from src.services.subject_service import generate_qr_share_details

@st.dialog("Share Subject Code & QR")
def share_subject_dialog(subject_name: str, subject_code: str):
    details = generate_qr_share_details(subject_name, subject_code)
    join_url = details["join_url"]
    qr_bytes = details["qr_png_bytes"]

    st.caption("Students can scan the QR code using their camera or enter the subject code directly to join this class.")

    col1, col2 = st.columns([1.2, 1], gap="medium", vertical_alignment="center")

    with col1:
        st.markdown("**Subject Code**")
        st.code(subject_code, language="text")

        st.markdown("**Direct Join Link**")
        st.code(join_url, language="text")

        st.info("Share this code or link with your students via email, LMS, or messaging apps.")

    with col2:
        st.image(qr_bytes, width="stretch", caption=f"Scan to join {subject_name}")

    st.divider()
    if st.button("Done", type="primary", width="stretch", key="share_modal_done_btn"):
        st.rerun()
