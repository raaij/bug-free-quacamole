"""Debug Panel Component - Shows session state and API responses"""

import streamlit as st
import json


def render_debug_panel():
    """
    Render a collapsible debug panel showing session state and API responses
    """

    with st.expander("🐛 Debug Panel (Development Only)", expanded=False):
        st.markdown("### Session State")

        # Upload Status
        st.markdown("**Upload Status:**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Status", st.session_state.get("upload_status", "idle"))
        with col2:
            st.metric("Progress", f"{st.session_state.get('progress', 0)}%")

        st.markdown("---")

        # Session Info
        st.markdown("**Session Information:**")
        session_id = st.session_state.get("session_id")
        if session_id:
            st.success(f"Session ID: `{session_id}`")
        else:
            st.info("No session ID yet - upload files to create session")

        st.markdown("---")

        # File Info
        st.markdown("**Uploaded Files:**")

        dataset_files = st.session_state.get("dataset_files")
        if dataset_files:
            st.write(f"✅ **Dataset Files ({len(dataset_files)}):**")
            for idx, dataset_file in enumerate(dataset_files):
                st.json({
                    f"File {idx + 1}": {
                        "name": dataset_file.name,
                        "size": f"{dataset_file.size / 1024:.2f} KB",
                        "type": dataset_file.type
                    }
                })
        else:
            st.write("❌ No dataset files uploaded")

        screenshot_file = st.session_state.get("screenshot_file")
        if screenshot_file:
            st.write("✅ **Screenshot File:**")
            st.json({
                "name": screenshot_file.name,
                "size": f"{screenshot_file.size / 1024:.2f} KB",
                "type": screenshot_file.type
            })
        else:
            st.write("❌ No screenshot file uploaded")

        clarification = st.session_state.get("clarification_text", "")
        if clarification:
            st.write("✅ **Clarification Text:**")
            st.text(clarification)

        st.markdown("---")

        # API Responses
        st.markdown("**API Responses:**")

        # Upload response
        datasets_info = st.session_state.get("datasets_info")
        screenshot_info = st.session_state.get("screenshot_info")
        if datasets_info or screenshot_info:
            st.write("📤 **Upload Response:**")
            with st.container():
                if datasets_info:
                    st.write(f"Datasets Info ({len(datasets_info)}):")
                    st.json(datasets_info)
                if screenshot_info:
                    st.write("Screenshot Info:")
                    st.json(screenshot_info)

        # DuckDB Metadata
        metadata = st.session_state.get("metadata")
        table_names = st.session_state.get("table_names", [])

        if metadata:
            st.write("🦆 **DuckDB Metadata:**")

            # Check if metadata is a list (multiple tables) or dict (single table)
            if isinstance(metadata, list):
                # Multiple tables
                st.write(f"**{len(metadata)} Table(s) Ingested:**")

                for idx, table_metadata in enumerate(metadata):
                    with st.expander(f"Table {idx + 1}: {table_names[idx] if idx < len(table_names) else 'Unknown'}", expanded=idx == 0):
                        # Show summary metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Rows", table_metadata.get("row_count", "N/A"))
                        with col2:
                            st.metric("Columns", table_metadata.get("column_count", "N/A"))
                        with col3:
                            st.metric("Table", table_metadata.get("table_name", "N/A"))

                        # Show column schema
                        columns = table_metadata.get("columns", [])
                        if columns:
                            st.write("**Column Schema:**")
                            schema_data = []
                            for col in columns:
                                schema_data.append({
                                    "Column": col.get("name"),
                                    "Type": col.get("type"),
                                    "Nullable": col.get("null", "YES")
                                })
                            st.dataframe(schema_data, use_container_width=True, hide_index=True)

                        # Show sample data
                        sample_data = table_metadata.get("sample_data", [])
                        if sample_data:
                            st.write("**Sample Data (first 5 rows):**")
                            st.dataframe(sample_data, use_container_width=True)

                        # Show full metadata JSON
                        if st.checkbox(f"Show Full Metadata JSON - Table {idx + 1}", key=f"show_full_metadata_{idx}"):
                            st.json(table_metadata)
            else:
                # Single table (backwards compatibility)
                # Show summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", metadata.get("row_count", "N/A"))
                with col2:
                    st.metric("Columns", metadata.get("column_count", "N/A"))
                with col3:
                    st.metric("Table", metadata.get("table_name", "N/A"))

                # Show column schema
                columns = metadata.get("columns", [])
                if columns:
                    st.write("**Column Schema:**")
                    schema_data = []
                    for col in columns:
                        schema_data.append({
                            "Column": col.get("name"),
                            "Type": col.get("type"),
                            "Nullable": col.get("null", "YES")
                        })
                    st.dataframe(schema_data, use_container_width=True, hide_index=True)

                # Show sample data
                sample_data = metadata.get("sample_data", [])
                if sample_data:
                    st.write("**Sample Data (first 5 rows):**")
                    st.dataframe(sample_data, use_container_width=True)

                # Show full metadata JSON
                if st.checkbox("Show Full Metadata JSON", key="show_full_metadata"):
                    st.json(metadata)
        else:
            st.info("No DuckDB metadata yet - complete ingestion step")

        # Agent Understanding
        agent_understanding = st.session_state.get("agent_understanding")
        if agent_understanding:
            st.write("🤖 **Agent Understanding:**")
            st.json(agent_understanding)
        else:
            st.info("No agent understanding yet - complete analysis step")

        st.markdown("---")

        # Errors
        upload_error = st.session_state.get("upload_error")
        if upload_error:
            st.error(f"**Error:** {upload_error}")

        st.markdown("---")

        # Full Session State
        if st.checkbox("Show Full Session State", key="show_full_session"):
            st.write("**Complete Session State:**")
            # Filter out file objects for display
            filtered_state = {}
            for key, value in st.session_state.items():
                if key not in ["dataset_files", "screenshot_file", "accumulated_dataset_files"]:
                    filtered_state[key] = str(value) if not isinstance(value, (dict, list, str, int, float, bool, type(None))) else value
            st.json(filtered_state)

        # Refresh button
        if st.button("🔄 Refresh Debug Panel", use_container_width=True):
            st.rerun()
