"""
Dialog for reviewing, adjusting, and confirming AI attendance results.
Provides interactive verification before database commit.
"""

from typing import Dict, Any, List
import streamlit as st
import pandas as pd
from src.services.attendance_service import confirm_and_save_attendance

def show_attendance_result(session_draft: Dict[str, Any]):
    """
    Renders an interactive review table allowing teachers to inspect AI detections,
    manually adjust student statuses, and idempotently commit to Supabase.
    """
    session_id = session_draft["session_id"]
    subject_id = session_draft["subject_id"]
    timestamp = session_draft["timestamp"]
    initial_df = session_draft["review_df"]
    mode = session_draft.get("mode", "face").capitalize()

    teacher_data = st.session_state.get("teacher_data", {})
    teacher_id = teacher_data.get("teacher_id")

    # Display Session Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Mode", mode)
    with m2:
        st.metric("Total Enrolled", session_draft.get("total_enrolled", len(initial_df)))
    with m3:
        st.metric("Initial Present", session_draft.get("present_count", 0))
    with m4:
        if mode == "Face":
            st.metric("Unknown Faces", session_draft.get("unknown_faces_count", 0))
        else:
            st.metric("Voice Check-Ins", session_draft.get("segments_processed", 0))

    if session_draft.get("unknown_faces_count", 0) > 0:
        st.warning(f"⚠️ {session_draft['unknown_faces_count']} face(s) in the photos were not recognized among enrolled students. Please review the roster below.")

    st.markdown("##### Student Roster Review")
    st.caption("You may override the attendance status of any student below before confirming.")

    # Configure editable data editor
    display_cols = ["Name", "Is Present", "Status", "Confidence", "Detected In"]
    clean_display_df = initial_df[display_cols].copy()

    edited_df = st.data_editor(
        clean_display_df,
        column_config={
            "Name": st.column_config.TextColumn("Student Name", disabled=True),
            "Is Present": st.column_config.CheckboxColumn("Present?", help="Toggle student presence", default=False),
            "Status": st.column_config.TextColumn("Detected Status", disabled=True),
            "Confidence": st.column_config.TextColumn("Confidence", disabled=True),
            "Detected In": st.column_config.TextColumn("Source", disabled=True),
        },
        hide_index=True,
        width="stretch",
        key=f"attendance_review_editor_{session_id}"
    )

    # Calculate real-time adjusted count
    current_present = int(edited_df["Is Present"].sum())
    current_absent = len(edited_df) - current_present
    st.caption(f"Final Count to Record: **{current_present} Present**, **{current_absent} Absent**")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Discard & Retry", width="stretch", key="dlg_att_discard_btn"):
            st.session_state.attendance_images = []
            st.session_state.voice_attendance_results = None
            st.session_state.active_attendance_session = None
            st.toast("Attendance session discarded.", icon="🗑️")
            st.rerun()

    with col2:
        is_saving = st.session_state.get("is_saving_attendance", False)
        if st.button("Confirm & Save Attendance", type="primary", width="stretch", disabled=is_saving, key="dlg_att_confirm_btn"):
            if not teacher_id:
                st.error("Authentication expired. Please log in again.")
                return

            st.session_state["is_saving_attendance"] = True

            # Prepare final logs from edited table
            final_records: List[Dict[str, Any]] = []
            for idx, row in edited_df.iterrows():
                sid = int(initial_df.iloc[idx]["student_id"])
                final_records.append({
                    "student_id": sid,
                    "subject_id": subject_id,
                    "timestamp": timestamp,
                    "is_present": bool(row["Is Present"])
                })

            success, msg = confirm_and_save_attendance(teacher_id, session_id, subject_id, final_records)
            st.session_state["is_saving_attendance"] = False

            if success:
                st.session_state.pop("_cached_teacher_subjects", None)
                st.session_state.pop("_cached_teacher_attendance_history", None)
                st.toast(msg, icon="✅")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.session_state.active_attendance_session = None
                st.session_state["attendance_success_toast"] = msg
                st.rerun()
            else:
                st.error(msg)

@st.dialog("Review Attendance Session", width="large")
def attendance_result_dialog(df_or_payload, logs_legacy=None):
    """
    Dialog entrypoint supporting both new session draft dicts and legacy arguments.
    """
    if isinstance(df_or_payload, dict):
        show_attendance_result(df_or_payload)
    else:
        # Reconstruct structured draft from legacy args
        df = df_or_payload
        subject_id = logs_legacy[0]["subject_id"] if logs_legacy else 0
        timestamp = logs_legacy[0]["timestamp"] if logs_legacy else ""
        draft = {
            "session_id": f"legacy_{int(pd.Timestamp.now().timestamp())}",
            "subject_id": subject_id,
            "timestamp": timestamp,
            "review_df": df.rename(columns={"ID": "student_id", "Source": "Detected In"}),
            "attendance_records": logs_legacy or [],
            "total_enrolled": len(df),
            "present_count": sum(1 for _, r in df.iterrows() if "Present" in str(r.get("Status", ""))),
            "mode": "face"
        }
        if "Is Present" not in draft["review_df"].columns:
            draft["review_df"]["Is Present"] = draft["review_df"]["Status"].apply(lambda s: "Present" in str(s))
        show_attendance_result(draft)
