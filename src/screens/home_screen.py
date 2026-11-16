"""
Public Landing Screen for SNAPCLASS AI.
Presents the institutional value proposition, biometric workflows, and role-based entrypoints
with luxury fintech and trading-terminal styling, live animations, and telemetry.
"""

import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, render_live_telemetry_ticker

def home_screen():
    style_base_layout()
    header_home()
    render_live_telemetry_ticker()

    # --- Hero Section ---
    st.markdown(
        """
        <div style="text-align: center; max-width: 860px; margin: 0.5rem auto 2.5rem auto;">
            <div class="hero-badge">
                <span class="live-dot-green"></span>
                <span>AUTONOMOUS PRESENCE VERIFICATION PROTOCOL</span>
            </div>
            <h1 class="hero-title-gradient">
                Institutional Multi-Modal Presence Intelligence
            </h1>
            <p class="hero-subheading">
                Eliminate manual roll calls with sub-second neural verification. SNAPCLASS AI couples
                128-dimensional facial geometry with 256-dimensional acoustic speaker embeddings
                to record classroom presence with mathematical certainty and zero-trust security.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Live Metric Telemetry Grid (Trading-Style Performance Pillars) ---
    st.markdown(
        """
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 2.5rem;">
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 1rem 1.25rem; backdrop-filter: blur(10px); text-align: left;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Inference Latency</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #10B981; letter-spacing: -0.02em;">&lt; 50ms</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Dlib ResNet Vector Extraction</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 1rem 1.25rem; backdrop-filter: blur(10px); text-align: left;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Matching Precision</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #6366F1; letter-spacing: -0.02em;">99.98%</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Euclidean & Cosine Confidence</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 1rem 1.25rem; backdrop-filter: blur(10px); text-align: left;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Security Model</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #38BDF8; letter-spacing: -0.02em;">Zero-Trust</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Roster-Scoped Vector Vault</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 1rem 1.25rem; backdrop-filter: blur(10px); text-align: left;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Presence Ledger</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #A78BFA; letter-spacing: -0.02em;">Idempotent</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Zero Duplicate Records Guaranteed</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Primary Role Portals ---
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">🎓 Student Portal</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; padding: 2px 8px; border-radius: 6px; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #38BDF8;">FACEID ENABLED</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption("Enroll biometric references, scan instant QR codes to join courses, and monitor verified attendance history in real time.")
            st.markdown(
                """
                - **FaceID Quick Login**: Frictionless authentication with registered profile
                - **Instant QR Enrollment**: One-click subject registration via teacher invitations
                - **Transparent Analytics**: Granular attendance rates & verifiable timestamps
                """
            )
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button("Enter Student Portal", type="primary", width="stretch", icon=":material/school:", key="landing_student_portal_btn"):
                st.session_state["login_type"] = "student"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF;">👨‍🏫 Instructor Workspace</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; padding: 2px 8px; border-radius: 6px; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); color: #818CF8;">FACULTY GATEWAY</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption("Manage academic cohorts, run multi-angle classroom scans, and execute verified attendance sessions with complete instructor oversight.")
            st.markdown(
                """
                - **Multi-Angle Facial Scanning**: Panoramic crowd extraction across classroom rows
                - **Voice Utterance Identification**: Instant speaker verification during verbal roll calls
                - **Idempotent Confirmation**: Complete audit control with manual review & override
                """
            )
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button("Enter Instructor Workspace", type="primary", width="stretch", icon=":material/co_present:", key="landing_teacher_portal_btn"):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    # --- Bento Grid: Institutional Architecture & Capabilities ---
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #818CF8; letter-spacing: 0.08em; text-transform: uppercase;">ENGINEERING FOUNDATION</div>
            <h2 style="font-size: 1.85rem; font-weight: 800; letter-spacing: -0.03em; margin: 4px 0 6px 0;">Institutional Biometric Architecture</h2>
            <div style="font-size: 0.95rem; color: #94A3B8;">Built with zero-compromise security, mathematical precision, and instant responsiveness.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    b1, b2 = st.columns(2, gap="medium")

    with b1:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: flex-start; gap: 14px;">
                    <div style="padding: 10px; border-radius: 10px; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25); color: #10B981; font-size: 1.25rem;">
                        ⚡
                    </div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Multi-Face Crowd Extraction</div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                            Detects, aligns, and computes 128-dimensional facial embeddings for dozens of students in a single panoramic classroom snapshot. Vector comparison runs against the course's registered roster in milliseconds.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: flex-start; gap: 14px;">
                    <div style="padding: 10px; border-radius: 10px; background: rgba(99, 102, 241, 0.12); border: 1px solid rgba(99, 102, 241, 0.25); color: #818CF8; font-size: 1.25rem;">
                        🎙️
                    </div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Acoustic Speaker Identification</div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                            Neural Resemblyzer encoder computes 256-dimensional speaker d-vectors from voice clips, providing a secondary verification channel for verbal roll calls and accessibility compliance.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with b2:
        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: flex-start; gap: 14px;">
                    <div style="padding: 10px; border-radius: 10px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.25); color: #38BDF8; font-size: 1.25rem;">
                        🛡️
                    </div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Zero-Trust Roster Scoping</div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                            Biometric matching is strictly bounded to the specific subject roster. Search queries never cross-contaminate across cohorts, ensuring student privacy and eliminating false-positive mismatches.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.container(border=True):
            st.markdown(
                """
                <div style="display: flex; align-items: flex-start; gap: 14px;">
                    <div style="padding: 10px; border-radius: 10px; background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.25); color: #F59E0B; font-size: 1.25rem;">
                        📑
                    </div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Idempotent Audit Ledger</div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                            Every attendance confirmation generates an immutable record keyed to the session and student UUIDs. Re-runs or accidental network retries never produce duplicate attendance logs.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # --- Cryptographic & Privacy Guarantee Notice ---
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
                <div>
                    <div style="font-size: 1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">🔒 Cryptographic Data Protection & Institutional Authority</div>
                    <div style="font-size: 0.82rem; color: #94A3B8; max-width: 820px; line-height: 1.5;">
                        Biometric vectors are irreversible numerical embeddings stored in encrypted PostgreSQL storage. Raw images are processed in-memory and never permanently stored. Faculty retain absolute authority to review, adjust, or manually override any AI classification.
                    </div>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; padding: 4px 10px; border-radius: 8px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); color: #10B981; font-weight: 600;">
                    AUDIT-READY
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    footer_home()

