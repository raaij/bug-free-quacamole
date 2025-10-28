"""Screen 2: Dashboard Screen - Displays the generated dashboard"""
import streamlit as st
import plotly.express as px
import pandas as pd
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
            value="Sales Performance Dashboard",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("🔄 Refresh"):
            st.success("Dashboard refreshed!")

    st.markdown("<hr>", unsafe_allow_html=True)

    # st.info("ℹ️ This is a sample dashboard. In a real app, the charts would be generated based on your uploaded sketch and data.")

    # Generate mock dashboard
    render_mock_dashboard()

    # Debug Panel
    st.markdown("<hr>", unsafe_allow_html=True)
    render_debug_panel()

def render_mock_dashboard():
    """Render a mock dashboard with sample visualizations"""
    # Create sample data
    df_revenue = pd.DataFrame({
        'Region': ['North', 'South', 'East', 'West', 'Central'],
        'Revenue': [45000, 38000, 52000, 41000, 35000]
    })
    df_sales = pd.DataFrame({
        'Date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']),
        'Sales': [100, 120, 110, 135, 150]
    })

    # Layout in 2 columns
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(
            df_revenue,
            x='Region',
            y='Revenue',
            title='Revenue by Region',
            color='Revenue',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(
            df_sales,
            x='Date',
            y='Sales',
            title='Sales Trend',
            markers=True
        )
        st.plotly_chart(fig2, use_container_width=True)
