from draw_dash.constant import PATH_DRAW_DASH

content = """
import streamlit as st
import plotly.express as px
import pandas as pd
from .components.debug_panel import render_debug_panel

def render():
    # Render dashboard view
    render_dashboard_panel()

def render_dashboard_panel():
    # Renders main dashboard panel

    ## Dashboard header
    col1, col2 = st.columns([8, 1])
    with col1:
        st.text_input(
            "Dashboard Title",
            value="Sales Performance Dashboard",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("🔄 Refresh"):
            st.success("Dashboard refreshed!")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Create dashboard
    create_dashboard()

    # Debug Panel
    st.markdown("<hr>", unsafe_allow_html=True)
    render_debug_panel()

def create_dashboard():
    # TODO: Modify this function

    # Create sample data

    # Query dataframes from DuckDB.

    # Create charts
    ...
"""

def initialize_dashboard():
    with open(PATH_DRAW_DASH / "frontend2" / "dashboard_screen.py", "w") as fp:
        fp.write(content)
