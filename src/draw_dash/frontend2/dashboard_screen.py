
import streamlit as st
import plotly.express as px
import pandas as pd
import duckdb
from .components.debug_panel import render_debug_panel

def render():
    """Render the dashboard view"""
    render_dashboard_panel()

def render_dashboard_panel():
    """Render the main dashboard panel"""
    # Dashboard header
    col1, col2 = st.columns([8, 1])
    with col1:
        st.text_input(
            "Dashboard Title",
            value="Marketing Balance Histogram",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("🔄 Refresh"):
            st.success("Dashboard refreshed!")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Generate the dashboard
    create_dashboard()

    # Debug Panel
    st.markdown("<hr>", unsafe_allow_html=True)
    render_debug_panel()

def create_dashboard():
    """
    This function connects to a DuckDB database, executes a query to fetch balance data
    from the 'marketing' table, and displays it as a histogram using Streamlit and Plotly.
    """
    # --- Database Connection and Query ---
    try:
        con = duckdb.connect(database=':memory:', read_only=False)
        
        # Note: In a real-world scenario, the data loading would be handled more robustly.
        # This assumes 'marketing.csv' is in a 'data' directory relative to the execution path.
        try:
            con.execute("CREATE TABLE marketing AS SELECT * FROM read_csv_auto('data/marketing.csv')")
        except duckdb.IOException as e:
            st.error("Failed to load data. Make sure 'data/marketing.csv' is available.")
            st.error(f"Details: {e}")
            return
            
        query = "SELECT BALANCE FROM marketing"
        df = con.execute(query).fetchdf()
        con.close()

    except Exception as e:
        st.error(f"An error occurred during database operation: {e}")
        return

    # --- Chart Generation ---
    if not df.empty:
        # Create the histogram
        fig = px.histogram(df, x="BALANCE")

        # --- Apply Specifications from JSON ---
        
        # Layout updates
        fig.update_layout(
            title_text="HISTOGRAM",
            xaxis_title="bin",
            yaxis_title="balance",
            showlegend=False,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        
        # Trace style updates
        fig.update_traces(
            marker_color="#1f77b4"
        )

        # --- Display Chart ---
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("The query returned no data.")

