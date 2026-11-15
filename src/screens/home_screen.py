"""
Public Landing Screen for SNAPCLASS AI.
Presents the product value proposition, biometric workflows, and direct role-based entrypoints.
"""

import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout

def home_screen():
    style_base_layout()
    header_home()

    # --- Hero Section ---
    st.markdown(
        """
        <div style="text-align: center; max-width: 800px; margin: 0 auto 2.5rem auto;">
            <h1 style="font-size: 2.75rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 0.75rem;">
                Making Classroom Attendance Effortless with Multi-Modal AI
            </h1>
            <p style="font-size: 1.15rem; opacity: 0.8; line-height: 1.6; margin-bottom: 1.5rem;">
                Eliminate manual roll calls. SNAPCLASS AI combines deep facial embeddings and speaker recognition
                to verify classroom presence in seconds with complete instructor oversight.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Primary Role Portals ---
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown("### 🎓 Student Portal")
            st.caption("Enroll biometric profiles, join course sections with QR codes, and review verified attendance logs.")
            st.markdown(
                """
                - **FaceID Quick Login** with registered profile
                - **One-Click Enrollment** via QR invitation
                - **Transparent Records** & personal attendance rate
                """
            )
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button("Enter Student Portal", type="primary", width="stretch", icon=":material/school:", key="landing_student_portal_btn"):
                st.session_state["login_type"] = "student"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 👨‍🏫 Instructor Workspace")
            st.caption("Manage academic subjects, capture multi-angle classroom photos, and verify presence with full review controls.")
            st.markdown(
                """
                - **Multi-Face Photo Scanning** across panoramic angles
                - **Voice Utterance Identification** for speech roll calls
                - **Idempotent Confirmation** with manual override controls
                """
            )
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button("Enter Instructor Workspace", type="primary", width="stretch", icon=":material/co_present:", key="landing_teacher_portal_btn"):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    # --- Core Capabilities Showcase ---
    st.markdown("## How SNAPCLASS AI Works")
    st.caption("A streamlined, privacy-conscious workflow designed for modern campuses.")

    s1, s2, s3 = st.columns(3, gap="medium")

    with s1:
        with st.container(border=True):
            st.markdown("#### 1. Setup & Enrollment")
            st.caption(
                "Instructors create subjects and display instant QR codes. Students scan to enroll their facial and vocal reference vectors."
            )

    with s2:
        with st.container(border=True):
            st.markdown("#### 2. AI Multi-Modal Capture")
            st.caption(
                "Instructors take classroom photos or record verbal roll calls. Neural metric networks match candidates against enrolled rosters."
            )

    with s3:
        with st.container(border=True):
            st.markdown("#### 3. Verification & Records")
            st.caption(
                "AI provides suggestions. Instructors review, resolve ambiguous matches, and confirm attendance with audit-ready records."
            )

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # --- Security & Architecture Notice ---
    with st.container(border=True):
        st.markdown("#### 🛡️ Architecture & Data Protection")
        st.caption(
            "Biometric embeddings are 128-dimensional mathematical representations stored in encrypted cloud PostgreSQL (Supabase). "
            "Biometric candidate matching is strictly scoped to enrolled rosters per subject. Instructors retain final authority on all attendance records."
        )

    footer_home()
