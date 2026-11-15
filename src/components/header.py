"""
Header components for SNAPCLASS AI.
Provides clean brand presentation for public and authenticated dashboards.
"""

import streamlit as st

LOGO_URL = "https://i.ibb.co/YTYGn5qV/logo.png"

def header_home():
    """Header for public landing page."""
    c1, c2, c3 = st.columns([1, 4, 1], vertical_alignment="center")
    with c2:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: center; gap: 14px; margin-bottom: 1.5rem; margin-top: 1rem;">
                <img src="{LOGO_URL}" style="height: 60px; width: 60px; object-fit: contain; border-radius: 12px;" alt="SNAPCLASS AI Logo" />
                <div style="text-align: left;">
                    <span style="font-size: 1.75rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.2;">SNAPCLASS <span style="color: #6366F1;">AI</span></span>
                    <div style="font-size: 0.85rem; opacity: 0.7; font-weight: 500;">Next-Gen Biometric Attendance SaaS</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def header_dashboard():
    """Header for teacher and student dashboards."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
            <img src="{LOGO_URL}" style="height: 44px; width: 44px; object-fit: contain; border-radius: 8px;" alt="Logo" />
            <div style="text-align: left;">
                <span style="font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em;">SNAPCLASS <span style="color: #6366F1;">AI</span></span>
                <div style="font-size: 0.75rem; opacity: 0.65; font-weight: 500;">Academic Intelligence Platform</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
