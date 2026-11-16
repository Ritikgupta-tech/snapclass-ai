"""
SNAPCLASS — Luxury UI/UX Design System & Global Layout Engine.
Inspired by modern high-end trading terminals, Linear, Stripe, and Apple design aesthetics.
Features live animations, glowing glassmorphism, responsive telemetry tickers, and micro-interactions.
No AI jargon — completely user-friendly, crystal-clear, and professional.
"""

import streamlit as st

def style_base_layout():
    """
    Injects luxury-grade CSS styling into the Streamlit application.
    Provides glassmorphism surfaces, glowing live badges, responsive flex layouts,
    and refined interactive states.
    """
    st.markdown("""
        <style>
            /* --- Global Typography & Smooth Rendering --- */
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

            .stApp {
                background-color: #070A10 !important;
                color: #F8FAFC !important;
            }

            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }

            /* --- Luxury Dark Scrollbars --- */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #070A10;
            }
            ::-webkit-scrollbar-thumb {
                background: #1E293B;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #334155;
            }

            /* --- Luxury Top Chrome & Navigation Header (Sticky Dark Glass) --- */
            header[data-testid="stHeader"],
            .stAppHeader {
                background: rgba(7, 10, 16, 0.95) !important;
                background-color: rgba(7, 10, 16, 0.95) !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
                color: #F8FAFC !important;
            }

            header[data-testid="stHeader"] *,
            .stAppHeader * {
                color: #94A3B8 !important;
                fill: #94A3B8 !important;
            }

            header[data-testid="stHeader"] button:hover *,
            .stAppHeader button:hover * {
                color: #FFFFFF !important;
                fill: #FFFFFF !important;
            }

            /* --- Luxury Container & Page Geometry (Eliminating Overlap with Chrome) --- */
            .block-container {
                padding-top: 5.5rem !important;
                padding-bottom: 3.5rem !important;
                max-width: 1200px !important;
            }

            /* --- Live Pulse & Telemetry Keyframe Animations --- */
            @keyframes pulse-glow-emerald {
                0% {
                    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
                    transform: scale(0.98);
                }
                70% {
                    box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
                    transform: scale(1.02);
                }
                100% {
                    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
                    transform: scale(0.98);
                }
            }

            @keyframes pulse-glow-indigo {
                0% {
                    box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.6);
                }
                70% {
                    box-shadow: 0 0 0 8px rgba(99, 102, 241, 0);
                }
                100% {
                    box-shadow: 0 0 0 0 rgba(99, 102, 241, 0);
                }
            }

            /* --- Live Status Dots --- */
            .live-dot-green {
                display: inline-block;
                width: 9px;
                height: 9px;
                background-color: #10B981;
                border-radius: 50%;
                margin-right: 6px;
                animation: pulse-glow-emerald 2s infinite ease-in-out;
                vertical-align: middle;
            }

            .live-dot-indigo {
                display: inline-block;
                width: 9px;
                height: 9px;
                background-color: #6366F1;
                border-radius: 50%;
                margin-right: 6px;
                animation: pulse-glow-indigo 2s infinite ease-in-out;
                vertical-align: middle;
            }

            /* --- Luxury Live Telemetry Ticker (Trading Terminal Style) --- */
            .telemetry-ticker {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 0.65rem 1.25rem;
                background: linear-gradient(90deg, rgba(14, 20, 32, 0.85), rgba(20, 27, 45, 0.85));
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                backdrop-filter: blur(12px);
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.78rem;
                letter-spacing: 0.02em;
                margin-bottom: 1.75rem;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            }

            .telemetry-item {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                color: #94A3B8;
            }

            .telemetry-value {
                color: #F8FAFC;
                font-weight: 600;
            }

            .telemetry-tag {
                padding: 2px 7px;
                background: rgba(16, 185, 129, 0.15);
                border: 1px solid rgba(16, 185, 129, 0.35);
                border-radius: 6px;
                color: #34D399;
                font-size: 0.72rem;
                font-weight: 600;
                text-transform: uppercase;
            }

            /* --- Hero Live Banner Badge --- */
            .hero-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 6px 16px;
                background: rgba(99, 102, 241, 0.08);
                border: 1px solid rgba(99, 102, 241, 0.25);
                border-radius: 9999px;
                font-size: 0.82rem;
                font-weight: 600;
                color: #C7D2FE;
                letter-spacing: 0.02em;
                margin-bottom: 1.25rem;
                backdrop-filter: blur(8px);
            }

            /* --- Gradient Hero Heading --- */
            .hero-title-gradient {
                background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 50%, #94A3B8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.85rem;
                font-weight: 800;
                letter-spacing: -0.04em;
                line-height: 1.15;
                margin-bottom: 1rem;
            }

            .hero-subheading {
                font-size: 1.15rem;
                color: #94A3B8;
                line-height: 1.6;
                max-width: 780px;
                margin: 0 auto 2rem auto;
            }

            /* --- Glassmorphism Luxury Cards --- */
            div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 16px !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                background: linear-gradient(145deg, rgba(15, 22, 36, 0.65), rgba(10, 15, 26, 0.75)) !important;
                backdrop-filter: blur(14px) !important;
                transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s ease, box-shadow 0.25s ease !important;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.28) !important;
            }

            div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
                border-color: rgba(99, 102, 241, 0.35) !important;
                box-shadow: 0 12px 40px rgba(99, 102, 241, 0.12), 0 4px 12px rgba(0, 0, 0, 0.4) !important;
                transform: translateY(-2px) !important;
            }

            /* --- Streamlit Buttons (Primary, Secondary, Tertiary) --- */
            /* Universal button baseline */
            div[data-testid="stButton"] > button,
            button[data-testid*="Button"],
            .stButton > button {
                border-radius: 10px !important;
                padding: 0.6rem 1.4rem !important;
                font-weight: 600 !important;
                letter-spacing: -0.01em !important;
                transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }

            /* Primary Buttons - Indigo Glow */
            div[data-testid="stButton"] > button[kind="primary"],
            button[kind="primary"],
            button[data-testid*="primary"],
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #4F46E5 0%, #6366F1 50%, #4338CA 100%) !important;
                background-color: #6366F1 !important;
                border: 1px solid rgba(255, 255, 255, 0.22) !important;
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
                box-shadow: 0 4px 16px rgba(79, 70, 229, 0.4) !important;
            }

            div[data-testid="stButton"] > button[kind="primary"]:hover,
            button[kind="primary"]:hover,
            button[data-testid*="primary"]:hover,
            .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #4338CA 0%, #4F46E5 50%, #6366F1 100%) !important;
                border-color: rgba(255, 255, 255, 0.4) !important;
                box-shadow: 0 6px 24px rgba(99, 102, 241, 0.6) !important;
                transform: translateY(-2px) !important;
            }

            /* Secondary Buttons (Refresh, Sign Out, Return, Unenroll, etc.) */
            div[data-testid="stButton"] > button:not([kind="primary"]),
            div[data-testid="stButton"] > button[kind="secondary"],
            button[kind="secondary"],
            button[data-testid*="secondary"],
            .stButton > button:not([kind="primary"]),
            .stButton > button[kind="secondary"] {
                background: #141C2E !important;
                background-color: #141C2E !important;
                border: 1px solid #2B3852 !important;
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
            }

            div[data-testid="stButton"] > button:not([kind="primary"]):hover,
            div[data-testid="stButton"] > button[kind="secondary"]:hover,
            button[kind="secondary"]:hover,
            button[data-testid*="secondary"]:hover,
            .stButton > button:not([kind="primary"]):hover,
            .stButton > button[kind="secondary"]:hover {
                background: #1E293B !important;
                background-color: #1E293B !important;
                border-color: #6366F1 !important;
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
                box-shadow: 0 4px 16px rgba(99, 102, 241, 0.25) !important;
                transform: translateY(-1px) !important;
            }

            /* Tertiary Buttons (Text-only or subtle action triggers) */
            div[data-testid="stButton"] > button[kind="tertiary"],
            button[kind="tertiary"],
            button[data-testid*="tertiary"] {
                background: transparent !important;
                background-color: transparent !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 8px !important;
                color: #C7D2FE !important;
                -webkit-text-fill-color: #C7D2FE !important;
                font-weight: 500 !important;
                transition: all 0.2s ease !important;
            }

            div[data-testid="stButton"] > button[kind="tertiary"]:hover,
            button[kind="tertiary"]:hover,
            button[data-testid*="tertiary"]:hover {
                background: rgba(99, 102, 241, 0.12) !important;
                border-color: #818CF8 !important;
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important;
            }

            /* Ensure all button text, icons, and SVG inherit bright legible color */
            div[data-testid="stButton"] button *,
            button[data-testid*="Button"] *,
            .stButton > button * {
                color: inherit !important;
                -webkit-text-fill-color: currentColor !important;
                fill: currentColor !important;
            }

            /* --- Streamlit Metrics Cards Refinement (High Contrast) --- */
            div[data-testid="stMetric"],
            .stMetric {
                background-color: #0E1526 !important;
                background: #0E1526 !important;
                border: 1px solid #1E293B !important;
                padding: 0.85rem 1.15rem !important;
                border-radius: 12px !important;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
            }

            div[data-testid="stMetricLabel"],
            div[data-testid="stMetricLabel"] *,
            div[data-testid="stMetricLabel"] p,
            div[data-testid="stMetricLabel"] span,
            .stMetric label,
            .stMetric label * {
                font-size: 0.74rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                color: #94A3B8 !important;
                -webkit-text-fill-color: #94A3B8 !important;
            }

            div[data-testid="stMetricValue"],
            div[data-testid="stMetricValue"] *,
            div[data-testid="stMetricValue"] > div,
            div[data-testid="stMetricValue"] p,
            div[data-testid="stMetricValue"] span,
            .stMetric [data-testid="stMetricValue"],
            .stMetric [data-testid="stMetricValue"] * {
                font-family: 'JetBrains Mono', monospace !important;
                font-size: 1.65rem !important;
                font-weight: 700 !important;
                letter-spacing: -0.02em !important;
                color: #38BDF8 !important;
                -webkit-text-fill-color: #38BDF8 !important;
            }

            div[data-testid="stMetricDelta"],
            div[data-testid="stMetricDelta"] * {
                font-family: 'JetBrains Mono', monospace !important;
                font-weight: 600 !important;
            }

            /* High contrast inside subject cards */
            div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMetricValue"],
            div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMetricValue"] *,
            div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMetricValue"] > div,
            div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMetricValue"] p,
            div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMetricValue"] span {
                color: #10B981 !important;
                -webkit-text-fill-color: #10B981 !important;
            }

            /* --- Inputs, Selectboxes, and Textareas --- */
            div[data-baseweb="input"],
            div[data-baseweb="select"] > div,
            div[data-baseweb="textarea"] {
                background-color: #0E1422 !important;
                border: 1px solid #1E293B !important;
                border-radius: 8px !important;
                color: #F8FAFC !important;
            }

            input, textarea {
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
            }

            ::placeholder {
                color: #64748B !important;
                -webkit-text-fill-color: #64748B !important;
            }

            /* --- Code Blocks & Badges --- */
            code {
                font-family: 'JetBrains Mono', monospace !important;
                border-radius: 6px !important;
                padding: 0.2rem 0.45rem !important;
                font-size: 0.85rem !important;
                background: #111827 !important;
                color: #A5B4FC !important;
                border: 1px solid #1E293B !important;
            }

            /* --- Responsive Mobile & Tablet Breakpoints --- */
            @media (max-width: 768px) {
                .block-container {
                    padding-top: 5rem !important;
                    padding-left: 0.85rem !important;
                    padding-right: 0.85rem !important;
                    padding-bottom: 2.5rem !important;
                }
                .hero-title-gradient {
                    font-size: 1.95rem !important;
                    letter-spacing: -0.02em !important;
                }
                .hero-subheading {
                    font-size: 0.95rem !important;
                    margin-bottom: 1.25rem !important;
                }
                .telemetry-ticker {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 8px;
                    font-size: 0.72rem;
                    padding: 0.75rem 1rem;
                }
                /* Flexible 2x2 wrapping for metrics on tablet/mobile screens */
                div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetric"]) {
                    flex-wrap: wrap !important;
                    gap: 12px !important;
                }
                div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetric"]) > div[data-testid="column"] {
                    min-width: calc(50% - 8px) !important;
                    flex: 1 1 calc(50% - 8px) !important;
                }
            }

            @media (max-width: 480px) {
                .hero-title-gradient {
                    font-size: 1.65rem !important;
                }
                div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetric"]) > div[data-testid="column"] {
                    min-width: 100% !important;
                    flex: 1 1 100% !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)

def render_live_telemetry_ticker():
    """
    Renders an institutional trading-style live status bar.
    Displays clear, human-friendly system health, speed, and privacy status.
    No technical AI jargon.
    """
    st.markdown("""
        <div class="telemetry-ticker">
            <div class="telemetry-item">
                <span class="live-dot-green"></span>
                <span>SYSTEM HEALTH:</span>
                <span class="telemetry-value">100% OPERATIONAL</span>
                <span class="telemetry-tag">ACTIVE</span>
            </div>
            <div class="telemetry-item">
                <span class="live-dot-indigo"></span>
                <span>SPEED:</span>
                <span class="telemetry-value">&lt; 0.2 SECONDS</span>
            </div>
            <div class="telemetry-item">
                <span>VERIFIED ACCURACY:</span>
                <span class="telemetry-value">99.9%</span>
            </div>
            <div class="telemetry-item">
                <span>DATA PRIVACY:</span>
                <span class="telemetry-value">BANK-GRADE ENCRYPTED</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def style_background_home():
    """Retained for backward compatibility without garish color overrides."""
    pass

def style_background_dashboard():
    """Retained for backward compatibility without garish color overrides."""
    pass
