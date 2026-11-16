"""
Dialog for recording classroom audio and executing voice recognition attendance.
"""

import streamlit as st
from src.services.attendance_service import prepare_voice_attendance_session
from src.components.dialog_attendance_results import show_attendance_result

@st.dialog("Voice Attendance Session", width="large")
def voice_attendance_dialog(selected_subject_id: int):
    st.caption("Record classroom audio as students speak or answer roll call. SNAPCLASS will identify matching enrolled students instantly.")

    audio_data = st.audio_input("Record classroom roll call", key="voice_att_audio_input")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", width="stretch", key="dlg_voice_cancel_btn"):
            st.session_state.voice_attendance_results = None
            st.rerun()

    with col2:
        if st.button("Identify Voices & Take Attendance", width="stretch", type="primary", key="dlg_voice_analyze_btn"):
            if not audio_data:
                st.warning("Please record audio before clicking Analyze.")
                return

            with st.spinner("Listening to voice recording and matching students..."):
                try:
                    audio_bytes = audio_data.getvalue() if hasattr(audio_data, "getvalue") else audio_data.read()
                except Exception as e:
                    st.error(f"Could not read audio stream: {e}")
                    return

                teacher_data = st.session_state.get("teacher_data", {})
                teacher_id = teacher_data.get("teacher_id")
                success, msg, session_payload = prepare_voice_attendance_session(selected_subject_id, audio_bytes, teacher_id=teacher_id)
                if success and session_payload:
                    st.session_state["voice_attendance_results"] = session_payload
                    st.rerun()
                else:
                    st.error(msg)

    # Render review table if voice analysis was completed
    if st.session_state.get("voice_attendance_results"):
        st.divider()
        st.subheader("Review Identified Students")
        show_attendance_result(st.session_state["voice_attendance_results"])
