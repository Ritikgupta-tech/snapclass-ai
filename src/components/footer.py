"""
Footer components for SNAPCLASS AI.
Provides institutional-grade footer with privacy protection markers and system status.
"""

import streamlit as st

def footer_home():
    """Footer for public landing page with institutional status."""
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; padding: 1rem 0; font-size: 0.8rem; color: #64748B;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-weight: 700; color: #94A3B8;">SNAPCLASS AI</span>
                <span>•</span>
                <span>Automated Classroom Attendance SaaS</span>
                <span>•</span>
                <span>© 2026 Enterprise Edition</span>
            </div>
            <div style="display: flex; align-items: center; gap: 18px; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">
                <span style="display: inline-flex; align-items: center; gap: 6px;">
                    <span class="live-dot-green"></span>
                    <span style="color: #10B981;">ALL SYSTEMS OPERATIONAL</span>
                </span>
                <span style="color: #94A3B8;">SPEED: &lt; 0.2s</span>
                <span style="color: #94A3B8;">PRIVACY: 100% PROTECTED</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def footer_dashboard():
    """Footer for operational dashboards with privacy and audit indicators."""
    st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; padding: 0.75rem 0; font-size: 0.78rem; color: #64748B;">
            <div>
                <span style="font-weight: 600; color: #94A3B8;">SNAPCLASS AI Workspace</span>
                <span style="margin: 0 8px;">•</span>
                <span>Student privacy protected • Encrypted records scoped to course rosters</span>
            </div>
            <div style="display: flex; align-items: center; gap: 12px; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">
                <span class="live-dot-green"></span>
                <span style="color: #10B981; font-weight: 600;">SESSION ACTIVE & SECURED</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


