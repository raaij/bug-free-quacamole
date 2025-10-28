"""Screen 2: Chat Screen - Agent shows understanding and gets confirmation"""

import streamlit as st
from src.draw_dash.frontend.state import navigate_to
from src.draw_dash.frontend.components.debug_panel import render_debug_panel
from src.draw_dash.frontend.api_client import api_client


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
        # Display number of datasets
        if st.session_state.dataset_files:
            num_files = len(st.session_state.dataset_files)
            st.caption(f"Datasets: {num_files} file{'s' if num_files > 1 else ''}")
        else:
            st.caption("Datasets: N/A")

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

        # Debug Panel
        st.markdown("<br><br>", unsafe_allow_html=True)
        render_debug_panel()


def generate_initial_agent_message():
    """Generate the initial agent message showing understanding"""

    # Call the vision agent with screenshot and database metadata
    try:
        # Get screenshot bytes
        if not hasattr(st.session_state, 'screenshot_file') or st.session_state.screenshot_file is None:
            return "Error: No screenshot found. Please go back and upload a screenshot."

        st.session_state.screenshot_file.seek(0)
        screenshot_bytes = st.session_state.screenshot_file.read()
        screenshot_filename = st.session_state.screenshot_file.name

        # Get database metadata from ingestion response
        database_metadata = {}
        if hasattr(st.session_state, 'ingestion_response'):
            tables = st.session_state.ingestion_response.get('tables', [])
            database_metadata = {
                "tables": [
                    {
                        "table_name": table.get('table_name'),
                        "columns": table.get('columns', []),
                        "row_count": table.get('row_count')
                    }
                    for table in tables
                ]
            }

        # Call vision agent
        with st.spinner("🤖 Analyzing your sketch with AI..."):
            vision_result = api_client.call_vision_agent(
                screenshot_bytes=screenshot_bytes,
                screenshot_filename=screenshot_filename,
                database_metadata=database_metadata,
                user_notes=st.session_state.clarification_text
            )

        # Store the vision agent result in session state
        st.session_state.vision_agent_result = vision_result

        # Format the response
        clarification_note = ""
        if st.session_state.clarification_text:
            clarification_note = f"\n**Your Notes:** {st.session_state.clarification_text}\n"

        existing_cols = vision_result.get('already_existing_columns', [])
        calculated_cols = vision_result.get('calculation_needed', [])

        message = f"""
👋 I've analyzed your screenshot and database. Here's what I found:

📊 **Data Requirements Analysis**

**Columns Available in Database**:
{chr(10).join(f'- ✅ {col}' for col in existing_cols) if existing_cols else '- None detected'}

**Calculations/Aggregations Needed**:
{chr(10).join(f'- 🧮 {col}' for col in calculated_cols) if calculated_cols else '- None detected'}

**Database Schema**:
"""

        # Add table info
        if database_metadata.get('tables'):
            for table in database_metadata['tables']:
                message += f"\n**Table:** `{table['table_name']}` ({table['row_count']} rows)"
                # Extract column names to avoid nested f-string issues
                column_names = ', '.join([f"`{c['name']}`" for c in table['columns'][:10]])
                message += f"\n**Columns:** {column_names}"
                if len(table['columns']) > 10:
                    message += f" ... ({len(table['columns'])} total)"
                message += "\n"

        message += f"""
{clarification_note}
---

Does this match your requirements? You can:
- ✅ Reply "Looks good!" to generate the dashboard
- ✏️ Request changes or corrections
- ➕ Add more details about the visualization
"""

        return message

    except Exception as e:
        # Fallback to placeholder message if vision agent fails
        error_message = f"""
⚠️ I encountered an issue analyzing your screenshot: {str(e)}

I'll use a placeholder analysis for now. Here's a sample understanding:

📊 **Dashboard Title**: Sample Dashboard

**Sample Visualizations**:
1. Bar Chart - Data by Category
2. Line Chart - Trend Over Time

Please note: This is a placeholder. For accurate analysis, ensure:
- The ADK API server is running with proper API keys
- The vision_agent is properly configured
- The screenshot is readable

---

You can still proceed by replying "Looks good!" or requesting changes.
"""
        return error_message
