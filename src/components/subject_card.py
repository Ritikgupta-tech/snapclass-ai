"""
Reusable subject presentation card component for SNAPCLASS AI.
Uses trading-terminal inspired card styling, monospace badges, and high-contrast metrics.
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
    Renders a luxury, institutional card for academic course subjects.
    """
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 0.75rem;">
                <div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.01em;">{name}</div>
                    <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 2px;">
                        Section: <span style="color: #E2E8F0; font-weight: 600;">{section}</span>
                    </div>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; padding: 3px 8px; border-radius: 6px; background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.3); color: #C7D2FE; font-weight: 600; letter-spacing: 0.05em;">
                    {code}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if stats:
            stat_cols = st.columns(len(stats))
            for idx, (icon, label, value) in enumerate(stats):
                with stat_cols[idx]:
                    st.metric(label=f"{icon} {label}", value=value)

        if footer_callback:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            footer_callback()

