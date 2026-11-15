"""
Dialog for capturing camera snapshots and uploading classroom photos for face attendance.
"""

from typing import List
import streamlit as st
from PIL import Image
import io

@st.dialog("Add Classroom Photos")
def add_photos_dialog():
    st.caption("Upload or capture high-resolution photos of your classroom. Multiple angles are recommended for complete coverage.")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "dialog_photo_mode" not in st.session_state:
        st.session_state.dialog_photo_mode = "upload"

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        type_up = "primary" if st.session_state.dialog_photo_mode == "upload" else "tertiary"
        if st.button("Upload Files", type=type_up, width="stretch", key="dlg_mode_upload_btn"):
            st.session_state.dialog_photo_mode = "upload"
            st.rerun()

    with col_btn2:
        type_cam = "primary" if st.session_state.dialog_photo_mode == "camera" else "tertiary"
        if st.button("Use Camera", type=type_cam, width="stretch", key="dlg_mode_camera_btn"):
            st.session_state.dialog_photo_mode = "camera"
            st.rerun()

    st.divider()

    if st.session_state.dialog_photo_mode == "upload":
        uploaded_files = st.file_uploader(
            "Select classroom image files",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="dlg_classroom_files_uploader"
        )

        if uploaded_files:
            st.caption(f"{len(uploaded_files)} file(s) selected.")
            if st.button("Import Selected Photos", type="primary", width="stretch", key="dlg_import_photos_btn"):
                added_count = 0
                for f in uploaded_files:
                    try:
                        img = Image.open(f)
                        img.load()
                        st.session_state.attendance_images.append(img)
                        added_count += 1
                    except Exception as e:
                        st.error(f"Failed to load {f.name}: {e}")

                if added_count > 0:
                    st.toast(f"Added {added_count} photo(s) to attendance session!", icon="📸")
                    st.rerun()

    elif st.session_state.dialog_photo_mode == "camera":
        cam_snap = st.camera_input("Snap Classroom", key="dlg_classroom_camera_input")
        if cam_snap:
            if st.button("Add Snapshot to Session", type="primary", width="stretch", key="dlg_commit_snap_btn"):
                try:
                    img = Image.open(cam_snap)
                    img.load()
                    st.session_state.attendance_images.append(img)
                    st.toast("Snapshot added!", icon="📸")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error reading snapshot: {e}")

    current_count = len(st.session_state.attendance_images)
    st.divider()
    st.caption(f"Current Session Gallery: **{current_count}** photo(s) queued.")

    if st.button("Done & Return to Workspace", width="stretch", key="dlg_photo_done_btn"):
        st.rerun()
