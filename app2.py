"""
DrawDash - Frontend 2: Dashboard Viewer
Main Streamlit application entry point for displaying the generated dashboard.
"""

import streamlit as st
from draw_dash.frontend2 import dashboard_screen
from draw_dash.frontend2.state import init_session_state

# Page configuration
st.set_page_config(
    page_title="DrawDash | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for the dashboard frontend
init_session_state()

# Load custom CSS
# Ensure the path is correct relative to where you run the streamlit app
try:
    with open("src/draw_dash/frontend2/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("styles.css not found. The app will run with default styling.")


def main():
    """
    Main application router for the dashboard viewer.
    """

    # In a real-world scenario, the session_id would be passed via URL query parameters
    # to link this frontend with the data processed by the upload frontend.
    # Example URL: http://localhost:8502?session_id=your_unique_session_id
    # query_params = st.query_params
    # session_id = query_params.get("session_id")
    #
    # if session_id:
    #     st.session_state.session_id = session_id
    #     st.toast(f"Loading dashboard for session: {session_id}")
    #     # In a real application, you would now use this session_id to make an
    #     # API call to fetch the specific dashboard configuration and data.
    # else:
    #     st.info("No session ID found in URL. Displaying a sample dashboard.", icon="ℹ️")


    # This frontend only has one screen: the dashboard
    dashboard_screen.render()


if __name__ == "__main__":
    main()
