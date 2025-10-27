"""Screen 2: Chat Screen - Agent shows understanding and gets confirmation"""

import streamlit as st
from src.draw_dash.frontend.state import navigate_to


def render():
    """Render the full-width chat screen"""

    # Header
    col1, col2, col3 = st.columns([1, 8, 1])

    with col1:
        if st.button("← Back"):
            # Reset state and go back to upload
            st.session_state.upload_status = "idle"
            st.session_state.progress = 0
            navigate_to("upload")

    with col2:
        st.markdown("### Review Requirements")

    with col3:
        st.caption(f"Dataset: {st.session_state.dataset_file.name if st.session_state.dataset_file else 'N/A'}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Main chat area (centered, max-width)
    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        # Initialize chat history with agent's understanding
        if not st.session_state.chat_history:
            initial_message = generate_initial_agent_message()
            st.session_state.chat_history = [
                {"role": "agent", "content": initial_message}
            ]

        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "agent":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("user"):
                    st.markdown(message["content"])

        # Chat input
        user_input = st.chat_input("Confirm or request changes...")

        if user_input:
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })

            # Check if user confirmed
            confirmation_keywords = ["looks good", "perfect", "generate", "yes", "correct", "confirmed"]
            if any(keyword in user_input.lower() for keyword in confirmation_keywords):
                # User confirmed - start generating dashboard
                st.session_state.chat_history.append({
                    "role": "agent",
                    "content": "Great! Generating your dashboard now... ⚙️"
                })
                st.session_state.is_confirmed = True
                st.rerun()

            else:
                # User requested changes - agent responds
                response = "I understand you'd like some changes. Let me update the specifications..."
                st.session_state.chat_history.append({
                    "role": "agent",
                    "content": response
                })
                st.rerun()

        # If confirmed, navigate to dashboard
        if st.session_state.is_confirmed:
            st.success("✓ Generating dashboard...")
            import time
            time.sleep(2)
            navigate_to("dashboard")

        # Quick action suggestions
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Quick actions:**")
        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            if st.button("✓ Looks good!", use_container_width=True):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": "Looks good!"
                })
                st.session_state.is_confirmed = True
                st.rerun()

        with col_b:
            if st.button("Add a filter", use_container_width=True):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": "Can you add a date filter?"
                })
                st.rerun()

        with col_c:
            if st.button("Change chart type", use_container_width=True):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": "Can you change the first chart to a line chart?"
                })
                st.rerun()

        with col_d:
            if st.button("Modify time range", use_container_width=True):
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": "Can you show data for the last 60 days instead?"
                })
                st.rerun()


def generate_initial_agent_message():
    """Generate the initial agent message showing understanding"""

    clarification_note = ""
    if st.session_state.clarification_text:
        clarification_note = f"\n**Your Notes:** {st.session_state.clarification_text}\n"

    message = f"""
👋 I've analyzed your screenshot and description. Here's what I understood:

📊 **Dashboard Title**: Sales Performance Dashboard

**Visualizations Requested**:

1. 📊 **Bar Chart**
   - Title: "Revenue by Region"
   - X-axis: Region
   - Y-axis: Total Revenue
   - Aggregation: Sum

2. 📈 **Line Chart**
   - Title: "Sales Trend Over Time"
   - X-axis: Date
   - Y-axis: Daily Sales
   - Time Range: Last 30 days

3. 🥧 **Pie Chart**
   - Title: "Market Share by Product Category"
   - Values: Percentage of total sales

**Filters Detected**:
- Date range: Last 30 days
- Region: All regions
{clarification_note}
**Additional Notes**:
- Color scheme: Blue gradient
- Show data labels on charts

---

Does this match your requirements? You can:
- ✅ Reply "Looks good!" to generate the dashboard
- ✏️ Request changes (e.g., "Change chart 2 to a bar chart")
- ➕ Add more visualizations
"""

    return message
