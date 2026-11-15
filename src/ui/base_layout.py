"""
Base UI layout and subtle presentation adjustments for SNAPCLASS AI.
Complements native Streamlit theming with refined card spacing and typography.
"""

import streamlit as st

def style_base_layout():
    """
    Subtle CSS refinements for padding, card borders, and smooth interaction states.
    Avoids aggressive DOM manipulation or color overrides.
    """
    st.markdown("""
        <style>
            /* Clean block container padding */
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 3rem !important;
                max-width: 1100px;
            }

            /* Refined button transitions */
            button[data-testid="baseButton-primary"],
            button[data-testid="baseButton-secondary"],
            button[data-testid="baseButton-tertiary"] {
                transition: all 0.15s ease-in-out !important;
                font-weight: 500 !important;
            }

            /* Clean metric card styles */
            div[data-testid="stMetric"] {
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
            }

            /* Responsive tables */
            div[data-testid="stDataFrame"] {
                border-radius: 6px;
            }
        </style>
    """, unsafe_allow_html=True)

def style_background_home():
    """Retained for backward compatibility without garish color overrides."""
    pass

def style_background_dashboard():
    """Retained for backward compatibility without garish color overrides."""
    pass
