"""
Reusable subject presentation card component for SNAPCLASS AI.
Uses native Streamlit containers and polished typography.
"""

from typing import List, Tuple, Any, Callable, Optional
import streamlit as st

def subject_card(
    name: str,
    code: str,
    section: str,
    stats: Optional[List[Tuple[str, str, Any]]] = None,
    footer_callback: Optional[Callable[[], None]] = None
):
    """
    Renders a clean, modern card for academic course subjects.
    """
    with st.container(border=True):
        col_hdr, col_badge = st.columns([3, 1], vertical_alignment="top")
        with col_hdr:
            st.markdown(f"### {name}")
            st.caption(f"Section: **{section}**")
        with col_badge:
            st.code(code, language="text")

        if stats:
            stat_cols = st.columns(len(stats))
            for idx, (icon, label, value) in enumerate(stats):
                with stat_cols[idx]:
                    st.metric(label=f"{icon} {label}", value=value)

        if footer_callback:
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            footer_callback()
