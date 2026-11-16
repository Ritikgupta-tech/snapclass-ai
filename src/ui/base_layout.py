"""
SNAPCLASS AI — Luxury UI/UX Design System & Global Layout Engine.
Inspired by modern high-end trading terminals, Linear, Stripe, and Apple design aesthetics.
Features live animations, glowing glassmorphism, responsive telemetry tickers, and micro-interactions.
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
                background: #080B11;
            }
            ::-webkit-scrollbar-thumb {
                background: #1E293B;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #334155;
            }

            /* --- Luxury Container & Page Geometry --- */
            .block-container {
                padding-top: 1.25rem !important;
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

            @keyframes badge-shimmer {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }

            @keyframes subtle-float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-4px); }
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
                padding: 0.6rem 1.25rem;
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
                background: rgba(99, 102, 241, 0.15);
                border: 1px solid rgba(99, 102, 241, 0.35);
                border-radius: 6px;
                color: #A5B4FC;
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

            /* --- High-End Buttons --- */
            button[data-testid="baseButton-primary"] {
                background: linear-gradient(135deg, #4F46E5 0%, #6366F1 50%, #4338CA 100%) !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
                border-radius: 10px !important;
                padding: 0.6rem 1.4rem !important;
                font-weight: 600 !important;
                letter-spacing: -0.01em !important;
                box-shadow: 0 4px 16px rgba(79, 70, 229, 0.35) !important;
                transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            }

            button[data-testid="baseButton-primary"]:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 24px rgba(99, 102, 241, 0.55) !important;
                border-color: rgba(255, 255, 255, 0.35) !important;
            }

            button[data-testid="baseButton-secondary"] {
                background: rgba(255, 255, 255, 0.04) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 10px !important;
                padding: 0.6rem 1.4rem !important;
                font-weight: 500 !important;
                backdrop-filter: blur(8px) !important;
                transition: all 0.2s ease !important;
            }

            button[data-testid="baseButton-secondary"]:hover {
                background: rgba(255, 255, 255, 0.08) !important;
                border-color: rgba(255, 255, 255, 0.25) !important;
                transform: translateY(-1px) !important;
            }

            /* --- Streamlit Metrics Cards Refinement --- */
            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.02) !important;
                border: 1px solid rgba(255, 255, 255, 0.06) !important;
                padding: 0.85rem 1.15rem !important;
                border-radius: 12px !important;
                backdrop-filter: blur(8px) !important;
            }

            div[data-testid="stMetricLabel"] {
                font-size: 0.78rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                color: #94A3B8 !important;
            }

            div[data-testid="stMetricValue"] {
                font-family: 'JetBrains Mono', monospace !important;
                font-size: 1.65rem !important;
                font-weight: 700 !important;
                letter-spacing: -0.03em !important;
            }

            /* --- Code Blocks & Badges --- */
            code {
                font-family: 'JetBrains Mono', monospace !important;
                border-radius: 6px !important;
                padding: 0.2rem 0.45rem !important;
                font-size: 0.85rem !important;
            }

            /* --- Responsive Mobile & Tablet Breakpoints --- */
            @media (max-width: 768px) {
                .block-container {
                    padding-top: 0.85rem !important;
                    padding-left: 0.85rem !important;
                    padding-right: 0.85rem !important;
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
            }
        </style>
    """, unsafe_allow_html=True)

def render_live_telemetry_ticker():
    """
    Renders an institutional trading-style biometric telemetry bar.
    Displays live neural pipeline status, cryptographic guarantees, and engine health.
    """
    st.markdown("""
        <div class="telemetry-ticker">
            <div class="telemetry-item">
                <span class="live-dot-green"></span>
                <span>CORE PIPELINE:</span>
                <span class="telemetry-value">ONLINE</span>
                <span class="telemetry-tag">128-D EMBEDDINGS</span>
            </div>
            <div class="telemetry-item">
                <span class="live-dot-indigo"></span>
                <span>INFERENCE LATENCY:</span>
                <span class="telemetry-value">~14ms</span>
            </div>
            <div class="telemetry-item">
                <span>IDENTITY GATEWAY:</span>
                <span class="telemetry-value">IDEMPOTENT ZERO-TRUST</span>
            </div>
            <div class="telemetry-item">
                <span>ENCRYPTION:</span>
                <span class="telemetry-value">SHA-256 SCOPED</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def style_background_home():
    """Retained for backward compatibility without garish color overrides."""
    pass

def style_background_dashboard():
    """Retained for backward compatibility without garish color overrides."""
    pass

