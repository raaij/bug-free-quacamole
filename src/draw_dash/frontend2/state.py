"""Session state management for the Dashboard frontend"""
import streamlit as st

def init_session_state():
    """Initialize session state variables for the dashboard"""
    # In a real app, the session_id would be retrieved from URL params
    if "session_id" not in st.session_state:
        st.session_state.session_id = "mock_session_id"

    if "dashboard_data" not in st.session_state:
        st.session_state.dashboard_data = None
