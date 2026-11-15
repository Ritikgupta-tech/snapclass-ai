"""
Footer components for SNAPCLASS AI.
"""

import streamlit as st

def footer_home():
    """Footer for public landing page."""
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    st.divider()
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.caption("© 2026 SNAPCLASS AI • Production-Grade Multi-Modal Attendance SaaS")
    with c2:
        st.caption("🔒 Privacy-First Biometric Security")
    with c3:
        st.caption("⚡ Powered by Supabase & Streamlit")

def footer_dashboard():
    """Footer for operational dashboards."""
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.divider()
    c1, c2 = st.columns([3, 1])
    with c1:
        st.caption("SNAPCLASS AI • Institutional Dashboard • All biometric data securely scoped")
    with c2:
        st.caption("System Status: **Operational**")
