"""
DrawDash - Transform sketches into dashboards instantly
Main Streamlit application entry point
"""

import streamlit as st
from draw_dash.frontend.screens import upload_screen, chat_screen, dashboard_screen
from draw_dash.frontend.state import init_session_state

# Page configuration
st.set_page_config(
    page_title="DrawDash",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
init_session_state()

# Load custom CSS
with open("src/draw_dash/frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    """Main application router"""

    # Determine which screen to show based on state
    if st.session_state.screen == "upload":
        upload_screen.render()
    elif st.session_state.screen == "chat":
        chat_screen.render()
    elif st.session_state.screen == "dashboard":
        dashboard_screen.render()


if __name__ == "__main__":
    main()