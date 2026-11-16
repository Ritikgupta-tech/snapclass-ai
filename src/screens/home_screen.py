"""
Public Landing Screen for SNAPCLASS AI.
Presents the institutional value proposition, smart attendance workflows, and role-based entrypoints
with luxury fintech and trading-terminal styling, live animations, and telemetry.
All AI jargon removed — 100% user-friendly, professional, and clear.
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
                <span>AUTOMATED CLASSROOM ATTENDANCE PLATFORM</span>
            </div>
            <h1 class="hero-title-gradient">
                Classroom Attendance, Perfectly Automated.
            </h1>
            <p class="hero-subheading">
                Take roll call for your entire lecture hall in under 3 seconds. SNAPCLASS combines
                smart facial recognition and voice check-in so instructors can focus on teaching
                rather than manual attendance, with guaranteed student privacy.
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
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Verification Speed</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #10B981; letter-spacing: -0.02em;">&lt; 1 Second</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Instant classroom crowd scan</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 1rem 1.25rem; backdrop-filter: blur(10px); text-align: left;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Recognition Accuracy</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #6366F1; letter-spacing: -0.02em;">99.9%</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Matched to enrolled course rosters</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 1rem 1.25rem; backdrop-filter: blur(10px); text-align: left;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Student Privacy</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #38BDF8; letter-spacing: -0.02em;">100% Safe</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Photos are never stored on servers</div>
            </div>
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 1rem 1.25rem; backdrop-filter: blur(10px); text-align: left;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Attendance Records</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #A78BFA; letter-spacing: -0.02em;">Real-Time</div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Zero duplicate entries guaranteed</div>
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
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; padding: 2px 8px; border-radius: 6px; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #38BDF8;">FACE SIGN-IN READY</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption("Sign in effortlessly with your face, scan QR codes to join course sections, and monitor your personal attendance history.")
            st.markdown(
                """
                - **Face Sign-In**: Quick, contact-free sign in from any camera
                - **One-Tap QR Join**: Scan your instructor's QR code to enroll in a second
                - **Personal Attendance History**: Real-time stats and percentage tracking
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
            st.caption("Manage course cohorts, capture classroom photos or voice check-ins, and confirm attendance with complete review authority.")
            st.markdown(
                """
                - **Panoramic Photo Roll Call**: Identify dozens of students across all rows in one snap
                - **Voice-Assisted Roll Call**: Identify students as they speak up during roll call
                - **Full Instructor Control**: Review detected students and manually adjust records anytime
                """
            )
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            if st.button("Enter Instructor Workspace", type="primary", width="stretch", icon=":material/co_present:", key="landing_teacher_portal_btn"):
                st.session_state["login_type"] = "teacher"
                st.rerun()

    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    # --- Bento Grid: Core Platform Capabilities ---
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #818CF8; letter-spacing: 0.08em; text-transform: uppercase;">HOW SNAPCLASS WORKS</div>
            <h2 style="font-size: 1.85rem; font-weight: 800; letter-spacing: -0.03em; margin: 4px 0 6px 0;">Smarter Attendance in 4 Simple Steps</h2>
            <div style="font-size: 0.95rem; color: #94A3B8;">Designed to save valuable lecture time while keeping student privacy completely secure.</div>
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
                        📸
                    </div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Panoramic Group Photos</div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                            Snap a single photo of your classroom from any angle. SNAPCLASS detects and identifies all present students simultaneously across all rows in under a second.
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
                        <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Voice-Activated Roll Call</div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                            Students simply say "Present" or answer roll call out loud. The system accurately recognizes each student's voice and marks them present automatically.
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
                        📲
                    </div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Instant QR Code Enrollment</div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                            Display an invitation QR code on your classroom projector. Students scan it from their phones to enroll into your course roster with a single tap.
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
                        📊
                    </div>
                    <div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">Verified, Exportable Records</div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.5;">
                            Review the recognized attendance list with full instructor override power. Export clean attendance summaries for university administration and grading.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # --- Privacy Guarantee Notice ---
    with st.container(border=True):
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
                <div>
                    <div style="font-size: 1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">🔒 Bank-Grade Privacy by Design</div>
                    <div style="font-size: 0.82rem; color: #94A3B8; max-width: 820px; line-height: 1.5;">
                        Student privacy is our top priority. Camera snapshots and audio recordings are processed in-memory and immediately discarded. Only secure, encrypted mathematical keys are retained. Original student photos are never saved to our servers.
                    </div>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; padding: 4px 10px; border-radius: 8px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); color: #10B981; font-weight: 600;">
                    PRIVACY PROTECTED
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    footer_home()


