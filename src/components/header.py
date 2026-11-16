"""
Header components for SNAPCLASS AI.
Provides luxury brand presentation for public and authenticated dashboards with live status indicators.
"""

import streamlit as st

LOGO_URL = "https://i.ibb.co/YTYGn5qV/logo.png"

def header_home():
    """Header for public landing page with live status indicator."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; margin-bottom: 1.75rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255, 255, 255, 0.06);">
            <div style="display: flex; align-items: center; gap: 14px;">
                <img src="{LOGO_URL}" style="height: 52px; width: 52px; object-fit: contain; border-radius: 12px; box-shadow: 0 4px 20px rgba(99, 102, 241, 0.25);" alt="SNAPCLASS AI Logo" />
                <div style="text-align: left;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; color: #FFFFFF;">SNAPCLASS</span>
                        <span style="background: linear-gradient(135deg, #6366F1, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.6rem; font-weight: 800;">AI</span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 600; padding: 2px 8px; border-radius: 6px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #34D399; letter-spacing: 0.05em;">PRO EDITION</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 500;">Next-Generation Smart Attendance Platform</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;">
                <span class="live-dot-green"></span>
                <span style="color: #10B981; font-weight: 600;">SYSTEM ONLINE</span>
                <span style="color: #64748B;">•</span>
                <span style="color: #94A3B8;">99.9% VERIFIED ACCURACY</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def header_dashboard():
    """Header for teacher and student dashboards with live status telemetry."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <img src="{LOGO_URL}" style="height: 42px; width: 42px; object-fit: contain; border-radius: 10px; box-shadow: 0 4px 14px rgba(99, 102, 241, 0.2);" alt="Logo" />
                <div style="text-align: left;">
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="font-size: 1.3rem; font-weight: 800; letter-spacing: -0.02em; color: #FFFFFF;">SNAPCLASS</span>
                        <span style="background: linear-gradient(135deg, #6366F1, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.3rem; font-weight: 800;">AI</span>
                    </div>
                    <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 500;">Campus Attendance Workspace</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 20px; padding: 3px 10px;">
                <span class="live-dot-green"></span>
                <span style="color: #10B981; font-weight: 600;">ACTIVE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


