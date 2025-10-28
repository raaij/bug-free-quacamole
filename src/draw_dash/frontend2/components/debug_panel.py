"""Debug Panel Component for the Dashboard Frontend"""
import streamlit as st


def render_debug_panel():
    """Render a collapsible debug panel showing dashboard state"""
    with st.expander("🐛 Debug Panel (Development Only)", expanded=False):
        st.markdown("### Dashboard State")

        session_id = st.session_state.get("session_id", "N/A")
        st.metric("Session ID", session_id)

        st.markdown("---")
        st.markdown("\*\*Dashboard Data (Mock):\*\*")
        dashboard_data = st.session_state.get("dashboard_data")
        if dashboard_data:
            st.json(dashboard_data)
        else:
            st.info("No specific dashboard data loaded.")
