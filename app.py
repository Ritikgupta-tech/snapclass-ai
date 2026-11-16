"""
SNAPCLASS AI — Application Entrypoint & Global Router.
Coordinates page configuration, session state initialization, routing, and query parameters.
"""

import streamlit as st

def init_session_state():
    """Ensure baseline session state keys are initialized safely."""
    defaults = {
        "login_type": None,
        "is_logged_in": False,
        "user_role": None,
        "teacher_data": None,
        "student_data": None,
        "attendance_images": [],
        "voice_attendance_results": None,
        "active_attendance_session": None,
        "current_teacher_tab": "take_attendance",
        "show_student_registration": False,
        "login_attempts_tracker": {}
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def main():
    st.set_page_config(
        page_title="SNAPCLASS AI — Multi-Modal Attendance SaaS",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    init_session_state()

    # Route based on navigation state (lazy imports prevent loading inactive subsystems)
    login_type = st.session_state.get("login_type")

    if login_type == "teacher":
        from src.screens.teacher_screen import teacher_screen
        teacher_screen()
    elif login_type == "student":
        from src.screens.student_screen import student_screen
        student_screen()
    else:
        from src.screens.home_screen import home_screen
        home_screen()

    # Handle QR Join Invitation Link
    join_code = st.query_params.get("join-code")
    if join_code:
        # Route unauthenticated or non-student users to student screen
        if st.session_state.get("login_type") != "student":
            st.session_state["login_type"] = "student"
            st.rerun()

        # If student is authenticated, show instant enrollment dialog
        if st.session_state.get("is_logged_in") and st.session_state.get("user_role") == "student":
            from src.components.dialog_auto_enroll import auto_enroll_dialog
            auto_enroll_dialog(join_code)

if __name__ == "__main__":
    main()
