"""
Teacher Workspace Screen for SNAPCLASS AI.
Provides authentication, subject management, multi-modal attendance taking, and comprehensive attendance history.
"""

from typing import Dict, Any, List
import streamlit as st
import pandas as pd
from datetime import datetime
import io

from src.ui.base_layout import style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

from src.database.db import get_teacher_subjects
from src.services.auth_service import login_teacher, register_teacher, logout
from src.services.attendance_service import (
    prepare_face_attendance_session,
    get_teacher_attendance_overview
)

def teacher_screen():
    style_base_layout()

    if "teacher_data" in st.session_state and st.session_state.get("is_logged_in"):
        teacher_dashboard()
    elif st.session_state.get("teacher_login_type") == "register":
        teacher_screen_register()
    else:
        teacher_screen_login()

# --- Authentication Views ---

def teacher_screen_login():
    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Return to Home", type="secondary", key="teacher_login_home_btn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### Instructor Login")
        st.caption("Sign in with your instructor account credentials to manage classes and verify attendance.")

        username = st.text_input("Username", placeholder="e.g. ananya_roy", key="teacher_login_username_input")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="teacher_login_password_input")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sign In", type="primary", width="stretch", icon=":material/login:", key="teacher_do_login_btn"):
                success, msg, teacher = login_teacher(username, password)
                if success:
                    st.toast("Welcome back!", icon="👋")
                    st.rerun()
                else:
                    st.error(msg)

        with col2:
            if st.button("Create Account", type="tertiary", width="stretch", icon=":material/person_add:", key="teacher_goto_register_btn"):
                st.session_state["teacher_login_type"] = "register"
                st.rerun()

    footer_dashboard()

def teacher_screen_register():
    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Return to Home", type="secondary", key="teacher_reg_home_btn"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("### Register Instructor Account")
        st.caption("Create a new instructor profile to begin managing courses and attendance rosters.")

        username = st.text_input("Username *", placeholder="e.g. ananya_roy", key="teacher_reg_username_input")
        name = st.text_input("Full Name *", placeholder="e.g. Dr. Ananya Roy", key="teacher_reg_name_input")
        pwd = st.text_input("Password *", type="password", placeholder="At least 8 characters with upper, lower, number", key="teacher_reg_pwd_input")
        pwd_confirm = st.text_input("Confirm Password *", type="password", placeholder="Re-enter password", key="teacher_reg_pwd_confirm_input")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Complete Registration", type="primary", width="stretch", icon=":material/how_to_reg:", key="teacher_do_register_btn"):
                success, msg = register_teacher(username, name, pwd, pwd_confirm)
                if success:
                    st.success(msg)
                    st.session_state["teacher_login_type"] = "login"
                    st.rerun()
                else:
                    st.error(msg)

        with col2:
            if st.button("Already have an account? Sign In", type="tertiary", width="stretch", key="teacher_back_to_login_btn"):
                st.session_state["teacher_login_type"] = "login"
                st.rerun()

    footer_dashboard()

# --- Authenticated Dashboard ---

def teacher_dashboard():
    teacher_data = st.session_state["teacher_data"]
    teacher_id = teacher_data["teacher_id"]

    # Top Navigation Bar
    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        header_dashboard()
        st.caption(f"Signed in as **{teacher_data.get('name', 'Instructor')}** (`{teacher_data.get('username')}`)")
    with c2:
        if st.button("Sign Out", type="secondary", icon=":material/logout:", width="stretch", key="teacher_signout_btn"):
            logout()
            st.rerun()

    # Overview Metrics Row
    subjects = get_teacher_subjects(teacher_id)
    total_students = sum(s.get("total_students", 0) for s in subjects)
    total_classes = sum(s.get("total_classes", 0) for s in subjects)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Subjects", len(subjects))
    with m2:
        st.metric("Enrolled Students", total_students)
    with m3:
        st.metric("Attendance Sessions", total_classes)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Tab Navigation
    if "current_teacher_tab" not in st.session_state:
        st.session_state["current_teacher_tab"] = "take_attendance"

    t1, t2, t3 = st.columns(3)
    with t1:
        type1 = "primary" if st.session_state["current_teacher_tab"] == "take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, width="stretch", icon=":material/ar_on_you:", key="nav_tab_take_att"):
            st.session_state["current_teacher_tab"] = "take_attendance"
            st.rerun()

    with t2:
        type2 = "primary" if st.session_state["current_teacher_tab"] == "manage_subjects" else "tertiary"
        if st.button("Manage Subjects", type=type2, width="stretch", icon=":material/book_ribbon:", key="nav_tab_subjects"):
            st.session_state["current_teacher_tab"] = "manage_subjects"
            st.rerun()

    with t3:
        type3 = "primary" if st.session_state["current_teacher_tab"] == "attendance_records" else "tertiary"
        if st.button("Attendance Records", type=type3, width="stretch", icon=":material/history_edu:", key="nav_tab_records"):
            st.session_state["current_teacher_tab"] = "attendance_records"
            st.rerun()

    st.divider()

    # Tab Content Routing
    if st.session_state["current_teacher_tab"] == "take_attendance":
        teacher_tab_take_attendance(subjects)
    elif st.session_state["current_teacher_tab"] == "manage_subjects":
        teacher_tab_manage_subjects(subjects, teacher_id)
    elif st.session_state["current_teacher_tab"] == "attendance_records":
        teacher_tab_attendance_records(teacher_id)

    footer_dashboard()

# --- Tab 1: Attendance Workspace ---

def teacher_tab_take_attendance(subjects: List[Dict[str, Any]]):
    st.subheader("Classroom Attendance Workspace")
    st.caption("Capture photos or classroom audio to automatically recognize enrolled students and record presence.")

    if not subjects:
        with st.container(border=True):
            st.info("💡 You have not created any subjects yet. Please create a subject in 'Manage Subjects' first.")
            if st.button("Create Your First Subject", type="primary", key="quick_create_sub_btn"):
                st.session_state["current_teacher_tab"] = "manage_subjects"
                st.rerun()
        return

    # Subject Selector
    subject_map = {f"{s['name']} ({s['subject_code']}) — {s.get('section', 'General')}": s["subject_id"] for s in subjects}
    selected_label = st.selectbox("Select Academic Subject *", options=list(subject_map.keys()), key="attendance_subject_selector")
    selected_subject_id = subject_map[selected_label]

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # Action Toolbar
    col_photo_btn, col_voice_btn = st.columns(2)

    with col_photo_btn:
        with st.container(border=True):
            st.markdown("##### 📸 Photo Attendance")
            st.caption("Upload or capture multi-angle classroom photos.")
            if st.button("Open Camera / Upload Photos", type="primary", width="stretch", icon=":material/photo_prints:", key="btn_open_photo_dialog"):
                add_photos_dialog()

    with col_voice_btn:
        with st.container(border=True):
            st.markdown("##### 🎙️ Voice Attendance")
            st.caption("Record vocal roll-calls for speaker identification.")
            if st.button("Start Voice Roll-Call", type="primary", width="stretch", icon=":material/mic:", key="btn_open_voice_dialog"):
                voice_attendance_dialog(selected_subject_id)

    # Photos Gallery Preview
    if "attendance_images" not in st.session_state:
        st.session_state["attendance_images"] = []

    images = st.session_state["attendance_images"]

    if images:
        st.markdown(f"##### Queued Classroom Photos ({len(images)})")
        gallery_cols = st.columns(min(4, len(images)))
        for idx, img in enumerate(images):
            with gallery_cols[idx % len(gallery_cols)]:
                st.image(img, width="stretch", caption=f"Photo {idx + 1}")

        c_clear, c_run = st.columns([1, 2])
        with c_clear:
            if st.button("Clear Photos", type="tertiary", icon=":material/delete:", width="stretch", key="clear_all_photos_btn"):
                st.session_state["attendance_images"] = []
                st.rerun()

        with c_run:
            if st.button("Run Facial Recognition Analysis", type="primary", icon=":material/analytics:", width="stretch", key="run_face_analysis_btn"):
                with st.spinner("Extracting facial embeddings and cross-referencing roster..."):
                    success, msg, session_payload = prepare_face_attendance_session(selected_subject_id, images)
                    if success and session_payload:
                        st.session_state["active_attendance_session"] = session_payload
                        attendance_result_dialog(session_payload)
                    else:
                        st.error(msg)

    # Open review modal if active session exists
    if st.session_state.get("active_attendance_session"):
        attendance_result_dialog(st.session_state["active_attendance_session"])

# --- Tab 2: Manage Subjects ---

def teacher_tab_manage_subjects(subjects: List[Dict[str, Any]], teacher_id: int):
    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        st.subheader("Manage Academic Subjects")
        st.caption("View and organize course sections, student enrollment numbers, and share invitation codes.")
    with c2:
        if st.button("Create New Subject", type="primary", icon=":material/add:", width="stretch", key="btn_open_create_subject"):
            create_subject_dialog(teacher_id)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if not subjects:
        with st.container(border=True):
            st.markdown("### No Subjects Created Yet")
            st.caption("Create your first academic subject above to start enrolling students and generating attendance codes.")
    else:
        # Loop cleanly over subjects
        cols = st.columns(2)
        for i, sub in enumerate(subjects):
            sub_id = sub["subject_id"]
            sub_name = sub["name"]
            sub_code = sub["subject_code"]
            sub_sec = sub.get("section", "General")

            stats = [
                ("👥", "Students", sub.get("total_students", 0)),
                ("📅", "Classes", sub.get("total_classes", 0))
            ]

            def make_share_callback(s_name=sub_name, s_code=sub_code):
                def callback():
                    if st.button(f"Share Code: {s_code}", icon=":material/share:", width="stretch", key=f"share_btn_{s_code}"):
                        share_subject_dialog(s_name, s_code)
                return callback

            with cols[i % 2]:
                subject_card(
                    name=sub_name,
                    code=sub_code,
                    section=sub_sec,
                    stats=stats,
                    footer_callback=make_share_callback()
                )

# --- Tab 3: Attendance Records ---

def teacher_tab_attendance_records(teacher_id: int):
    st.subheader("Institutional Attendance Records")
    st.caption("Historical log of confirmed attendance sessions with detailed roster roll-ups.")

    sessions = get_teacher_attendance_overview(teacher_id)

    if not sessions:
        with st.container(border=True):
            st.markdown("### No Attendance History Found")
            st.caption("Confirmed attendance sessions taken via photo or voice will appear here with student breakdown and export options.")
        return

    # Filter Toolbar
    subjects_available = sorted(list(set(s["subject_name"] for s in sessions)))
    col_filter1, col_filter2 = st.columns([2, 1])

    with col_filter1:
        sub_filter = st.selectbox("Filter by Subject", options=["All Subjects"] + subjects_available, key="records_sub_filter")
    with col_filter2:
        search_query = st.text_input("Search", placeholder="Search course or code...", key="records_search_input").strip().lower()

    filtered_sessions = sessions
    if sub_filter != "All Subjects":
        filtered_sessions = [s for s in filtered_sessions if s["subject_name"] == sub_filter]
    if search_query:
        filtered_sessions = [
            s for s in filtered_sessions
            if search_query in s["subject_name"].lower() or search_query in s["subject_code"].lower()
        ]

    st.markdown(f"Showing **{len(filtered_sessions)}** session(s)")

    # Render Sessions
    for idx, sess in enumerate(filtered_sessions):
        with st.container(border=True):
            c_info, c_badge = st.columns([3, 1], vertical_alignment="center")
            with c_info:
                st.markdown(f"#### {sess['subject_name']} (`{sess['subject_code']}`)")
                st.caption(f"Session Time: **{sess['formatted_time']}** • Section: {sess['section']}")
            with c_badge:
                st.metric("Attendance", f"{sess['present_count']} / {sess['total_students']}", delta=sess["attendance_rate"])

            # Expandable Roster Detail
            with st.expander("View Student Roster Detail", expanded=False):
                roster_data = []
                for rec in sess.get("records", []):
                    st_name = rec.get("students", {}).get("name", f"Student {rec.get('student_id')}")
                    is_pres = rec.get("is_present", False)
                    roster_data.append({
                        "Student ID": rec.get("student_id"),
                        "Name": st_name,
                        "Status": "✅ Present" if is_pres else "❌ Absent"
                    })

                df_roster = pd.DataFrame(roster_data)
                st.dataframe(df_roster, hide_index=True, width="stretch")

                # CSV Download
                csv_bytes = df_roster.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Session CSV",
                    data=csv_bytes,
                    file_name=f"attendance_{sess['subject_code']}_{sess['timestamp'][:10]}.csv",
                    mime="text/csv",
                    key=f"dl_csv_{idx}_{sess['timestamp'][:10]}"
                )
