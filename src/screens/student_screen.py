"""
Student Portal Screen for SNAPCLASS AI.
Provides FaceID authentication, biometric profile enrollment, course management, and attendance history.
"""

from typing import Dict, Any, List
import streamlit as st
import numpy as np
from PIL import Image
import time
import pandas as pd

from src.ui.base_layout import style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_enroll import enroll_dialog

from src.database.db import (
    get_all_students,
    get_student_attendance
)
from src.services.auth_service import (
    login_student_by_id,
    register_student,
    logout
)
from src.services.subject_service import (
    get_student_dashboard_data,
    unenroll_student_from_subject
)
from src.pipelines.face_pipeline import (
    get_face_embeddings,
    match_face_to_candidates
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.validators.image_validators import validate_and_prepare_image

def student_screen():
    style_base_layout()

    if "student_data" in st.session_state and st.session_state.get("is_logged_in"):
        student_dashboard()
    else:
        student_login_and_register_view()

# --- Student Login & Biometric Registration View ---

def student_login_and_register_view():
    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Return to Home", type="secondary", key="student_login_home_btn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### 👤 Student FaceID Sign In")
        st.caption("Center your face in the camera view to authenticate using your registered biometric face profile.")

        photo_source = st.camera_input("Position face in the frame", key="student_faceid_camera")

        show_registration_form = st.session_state.get("show_student_registration", False)

        if photo_source:
            try:
                pil_img = Image.open(photo_source)
                is_valid, err_msg, np_img = validate_and_prepare_image(pil_img)

                if is_valid and np_img is not None:
                    with st.spinner("Analyzing facial geometry..."):
                        encodings = get_face_embeddings(np_img)

                        if len(encodings) == 0:
                            st.warning("⚠️ No face detected in frame. Please ensure proper lighting and face the camera.")
                        elif len(encodings) > 1:
                            st.warning("⚠️ Multiple faces detected. Please ensure only you are visible in the frame.")
                        else:
                            # 1 single face detected; match against enrolled database students
                            student_candidates = get_all_students(include_embeddings=True)
                            sid, name, dist, status = match_face_to_candidates(
                                encodings[0],
                                student_candidates,
                                distance_threshold=0.55,
                                ambiguous_threshold=0.62
                            )

                            if sid is not None and status in ("HIGH_CONFIDENCE", "NEEDS_REVIEW"):
                                success, msg, student = login_student_by_id(sid)
                                if success:
                                    st.toast(f"Welcome back, {name}!", icon="👋")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(msg)
                            else:
                                st.info("Face not recognized in student registry. If you are a new student, please complete registration below.")
                                show_registration_form = True
            except Exception as e:
                st.error(f"Error processing camera input: {e}")

        # Fallback registration button if not auto-triggered
        if not show_registration_form:
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            if st.button("New student? Register profile", type="tertiary", key="toggle_reg_form_btn"):
                st.session_state["show_student_registration"] = True
                st.rerun()

    # Registration Form Container
    if show_registration_form:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### 📝 Register Student Biometric Profile")
            st.caption("Enter your legal name and enroll facial and optional voice references.")

            new_name = st.text_input("Full Name *", placeholder="e.g. Ritik Gupta", key="student_reg_name_input")

            st.markdown("##### Step 1: Facial Snapshot")
            st.caption("The camera snapshot above will be used to generate your 128-dimensional facial reference embedding.")

            st.markdown("##### Step 2: Optional Voice Profile")
            st.caption("Enroll a voice reference to enable voice roll-call attendance.")

            audio_data = st.audio_input("Record phrase: 'I am present and ready for class'", key="student_reg_audio_input")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Cancel Registration", width="stretch", key="student_reg_cancel_btn"):
                    st.session_state["show_student_registration"] = False
                    st.rerun()

            with col2:
                if st.button("Create Student Profile", type="primary", width="stretch", icon=":material/how_to_reg:", key="student_reg_submit_btn"):
                    if not (new_name or "").strip():
                        st.warning("Please enter your full name.")
                    elif not photo_source:
                        st.warning("Please capture your face using the camera above.")
                    else:
                        with st.spinner("Extracting biometric features..."):
                            try:
                                pil_img = Image.open(photo_source)
                                is_valid, _, np_img = validate_and_prepare_image(pil_img)
                                encodings = get_face_embeddings(np_img)

                                if not encodings:
                                    st.error("Could not capture facial features. Please ensure your face is well lit and clear.")
                                else:
                                    face_emb = encodings[0].tolist()

                                    # Process optional voice embedding
                                    voice_emb = None
                                    if audio_data:
                                        audio_bytes = audio_data.getvalue() if hasattr(audio_data, "getvalue") else audio_data.read()
                                        voice_emb = get_voice_embedding(audio_bytes)

                                    success, msg, student = register_student(new_name, face_emb, voice_emb)
                                    if success:
                                        st.success(msg)
                                        st.session_state["show_student_registration"] = False
                                        time.sleep(1.2)
                                        st.rerun()
                                    else:
                                        st.error(msg)
                            except Exception as e:
                                st.error(f"Registration error: {e}")

    footer_dashboard()

# --- Authenticated Student Dashboard ---

def student_dashboard():
    student_data = st.session_state["student_data"]
    student_id = student_data["student_id"]
    student_name = student_data.get("name", "Student")

    # Header with sign out
    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
        st.caption(f"Student Portal • Welcome, **{student_name}** (`ID: #{student_id}`)")
    with c2:
        if st.button("Sign Out", type="secondary", icon=":material/logout:", width="stretch", key="student_signout_btn"):
            logout()
            st.rerun()

    # Load Enrolled Subjects & Overall Attendance
    subjects, summary = get_student_dashboard_data(student_id)

    # Overview Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Enrolled Courses", summary["enrolled_count"])
    with m2:
        st.metric("Total Classes Held", summary["total_classes"])
    with m3:
        st.metric("Classes Attended", summary["total_attended"])
    with m4:
        st.metric("Overall Attendance", f"{summary['overall_pct']}%")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Action Toolbar
    col_hdr, col_btn = st.columns([3, 1], vertical_alignment="center")
    with col_hdr:
        st.subheader("Your Enrolled Subjects")
    with col_btn:
        if st.button("Enroll in Subject", type="primary", icon=":material/add:", width="stretch", key="student_open_enroll_btn"):
            enroll_dialog()

    st.divider()

    if not subjects:
        with st.container(border=True):
            st.markdown("### No Courses Enrolled")
            st.caption("You are not currently enrolled in any academic courses. Ask your instructor for the subject code or QR link to join.")
    else:
        cols = st.columns(2)
        for i, sub in enumerate(subjects):
            sid = sub["subject_id"]
            sname = sub["name"]
            scode = sub["subject_code"]
            ssec = sub["section"]

            stats = [
                ("📅", "Classes", sub["total_classes"]),
                ("✅", "Attended", sub["attended_classes"]),
                ("📊", "Rate", f"{sub['attendance_pct']}%")
            ]

            def make_unenroll_callback(subject_id=sid, course_name=sname):
                def callback():
                    if st.button("Unenroll from Course", type="tertiary", icon=":material/delete_forever:", width="stretch", key=f"unenroll_btn_{subject_id}"):
                        success, msg = unenroll_student_from_subject(student_id, subject_id)
                        if success:
                            st.toast(f"Unenrolled from {course_name}.", icon="👋")
                            st.rerun()
                        else:
                            st.error(msg)
                return callback

            with cols[i % 2]:
                subject_card(
                    name=sname,
                    code=scode,
                    section=ssec,
                    stats=stats,
                    footer_callback=make_unenroll_callback()
                )

    # Attendance History Section
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.subheader("Attendance History Log")

    raw_logs = get_student_attendance(student_id)
    if not raw_logs:
        st.caption("No attendance logs recorded yet.")
    else:
        history_rows = []
        for log in raw_logs:
            sub = log.get("subjects") or {}
            ts = log.get("timestamp") or ""
            try:
                dt_obj = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                formatted_date = dt_obj.strftime("%b %d, %Y - %I:%M %p")
            except Exception:
                formatted_date = ts

            history_rows.append({
                "Date & Time": formatted_date,
                "Course": sub.get("name", "Unknown"),
                "Code": sub.get("subject_code", "N/A"),
                "Section": sub.get("section", "N/A"),
                "Status": "✅ Present" if log.get("is_present") else "❌ Absent"
            })

        df_history = pd.DataFrame(history_rows)
        st.dataframe(df_history, hide_index=True, width="stretch")

    footer_dashboard()
