"""Session state management for DrawDash frontend"""

import streamlit as st


def init_session_state():
    """Initialize all session state variables"""

    # Screen navigation
    if "screen" not in st.session_state:
        st.session_state.screen = "upload"

    # Upload screen state
    if "dataset_file" not in st.session_state:
        st.session_state.dataset_file = None

    if "screenshot_file" not in st.session_state:
        st.session_state.screenshot_file = None

    if "clarification_text" not in st.session_state:
        st.session_state.clarification_text = ""

    if "upload_status" not in st.session_state:
        st.session_state.upload_status = "idle"  # idle, uploading, processing, complete

    if "progress" not in st.session_state:
        st.session_state.progress = 0

    # Chat screen state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "agent_understanding" not in st.session_state:
        st.session_state.agent_understanding = None

    if "is_typing" not in st.session_state:
        st.session_state.is_typing = False

    if "is_confirmed" not in st.session_state:
        st.session_state.is_confirmed = False

    # Dashboard screen state
    if "dashboard_data" not in st.session_state:
        st.session_state.dashboard_data = None

    if "is_updating" not in st.session_state:
        st.session_state.is_updating = False

    if "is_fullscreen" not in st.session_state:
        st.session_state.is_fullscreen = False

    if "is_chat_visible" not in st.session_state:
        st.session_state.is_chat_visible = True


def reset_state():
    """Reset all session state (for starting over)"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()


def navigate_to(screen: str):
    """Navigate to a different screen"""
    st.session_state.screen = screen
    st.rerun()
