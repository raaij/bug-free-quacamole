"""Screen 3: Dashboard Screen - Split view with chat and dashboard"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.draw_dash.frontend.state import navigate_to


def render():
    """Render the dashboard split view"""

    if st.session_state.is_fullscreen:
        render_fullscreen_dashboard()
    else:
        render_split_view()


def render_split_view():
    """Render the split view with chat on left and dashboard on right"""

    # Create two columns for split view
    if st.session_state.is_chat_visible:
        chat_col, dashboard_col = st.columns([3, 7])
    else:
        chat_col = None
        dashboard_col = st.container()

    # Left Panel: Chat
    if st.session_state.is_chat_visible and chat_col:
        with chat_col:
            render_chat_panel()

    # Right Panel: Dashboard
    with dashboard_col if chat_col else dashboard_col:
        render_dashboard_panel()


def render_chat_panel():
    """Render the chat panel on the left"""

    st.markdown("### 💬 Chat")

    # Collapse chat button
    if st.button("Hide Chat ◀", use_container_width=True):
        st.session_state.is_chat_visible = False
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Add system message about dashboard being ready
    if len(st.session_state.chat_history) > 0:
        last_message = st.session_state.chat_history[-1]
        if "Generating your dashboard" not in last_message["content"]:
            st.session_state.chat_history.append({
                "role": "agent",
                "content": "✅ Dashboard generated! You can now request refinements."
            })

    # Display chat history
    chat_container = st.container(height=400)
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "agent":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("user"):
                    st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input("Request changes or refinements...")

    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Agent response (mock)
        response = "I'm updating the dashboard based on your request... ⚙️"
        st.session_state.chat_history.append({
            "role": "agent",
            "content": response
        })

        st.rerun()

    # Suggested refinements
    st.markdown("**Quick actions:**")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎨 Change colors", use_container_width=True, key="color"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Can you change the color scheme to green?"
            })
            st.rerun()

        if st.button("📥 Export", use_container_width=True, key="export"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Can you export this dashboard as HTML?"
            })
            st.rerun()

    with col2:
        if st.button("🔍 Add filters", use_container_width=True, key="filter"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Can you add a date range filter?"
            })
            st.rerun()

        if st.button("📊 Change type", use_container_width=True, key="type"):
            st.session_state.chat_history.append({
                "role": "user",
                "content": "Can you change the pie chart to a bar chart?"
            })
            st.rerun()


def render_dashboard_panel():
    """Render the dashboard panel on the right"""

    # Dashboard header
    col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 1])

    with col1:
        dashboard_title = st.text_input(
            "Dashboard Title",
            value="Sales Performance Dashboard",
            label_visibility="collapsed"
        )

    with col2:
        if not st.session_state.is_chat_visible:
            if st.button("Show Chat ▶"):
                st.session_state.is_chat_visible = True
                st.rerun()

    with col3:
        if st.button("🔲 Maximize"):
            st.session_state.is_fullscreen = True
            st.rerun()

    with col4:
        if st.button("📥 Export"):
            st.info("Export functionality coming soon!")

    with col5:
        if st.button("🔄 Refresh"):
            st.success("Dashboard refreshed!")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Generate mock dashboard
    render_mock_dashboard()


def render_mock_dashboard():
    """Render a mock dashboard with sample visualizations"""

    # Create sample data
    df_revenue = pd.DataFrame({
        'Region': ['North', 'South', 'East', 'West', 'Central'],
        'Revenue': [45000, 38000, 52000, 41000, 35000]
    })

    df_sales = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'Sales': [100 + i * 5 + (i % 7) * 10 for i in range(30)]
    })

    df_category = pd.DataFrame({
        'Category': ['Electronics', 'Clothing', 'Food', 'Books', 'Other'],
        'Share': [30, 25, 20, 15, 10]
    })

    # Layout in 2 columns
    col1, col2 = st.columns(2)

    with col1:
        # Bar Chart: Revenue by Region
        fig1 = px.bar(
            df_revenue,
            x='Region',
            y='Revenue',
            title='Revenue by Region',
            color='Revenue',
            color_continuous_scale='Blues'
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Pie Chart: Market Share
        fig2 = px.pie(
            df_category,
            values='Share',
            names='Category',
            title='Market Share by Product Category',
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Full width: Line Chart
    fig3 = px.line(
        df_sales,
        x='Date',
        y='Sales',
        title='Sales Trend Over Time (Last 30 Days)',
        markers=True
    )
    fig3.update_traces(line_color='#2563eb')
    st.plotly_chart(fig3, use_container_width=True)

    # Show loading indicator if updating
    if st.session_state.is_updating:
        with st.spinner("Updating dashboard..."):
            import time
            time.sleep(1)
            st.session_state.is_updating = False
            st.rerun()


def render_fullscreen_dashboard():
    """Render dashboard in fullscreen mode"""

    # Header with exit button
    col1, col2 = st.columns([8, 1])

    with col1:
        st.markdown("## Sales Performance Dashboard")

    with col2:
        if st.button("Exit Fullscreen ✕", use_container_width=True):
            st.session_state.is_fullscreen = False
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Render dashboard
    render_mock_dashboard()

    # Floating chat button
    st.markdown("""
        <div style="position: fixed; bottom: 20px; right: 20px;">
            <button style="
                background: #2563eb;
                color: white;
                border: none;
                padding: 15px 20px;
                border-radius: 50%;
                font-size: 1.5rem;
                cursor: pointer;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            ">💬</button>
        </div>
    """, unsafe_allow_html=True)