"""Screen 1: Upload Screen - Dataset, Screenshot, and Text inputs"""

import streamlit as st
from PIL import Image
import time
from draw_dash.frontend.state import navigate_to
from draw_dash.frontend.api_client import api_client
from draw_dash.frontend.components.debug_panel import render_debug_panel


def render():
    """Render the upload screen"""

    # Header
    st.markdown("""
        <div class="main-header">
            <h1>📊 DrawDash</h1>
            <p>Transform sketches into dashboards instantly</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main upload area
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # Dataset Upload (Required)
        st.markdown("### 1. Dataset Upload <span class='required-star'>*</span>", unsafe_allow_html=True)
        st.markdown("Upload your data files (CSV, JSON, or Parquet) - Max 10MB per file")

        # Initialize accumulated files list if not exists
        if "accumulated_dataset_files" not in st.session_state:
            st.session_state.accumulated_dataset_files = []

        # Try native multiple file upload first
        dataset_files_uploaded = st.file_uploader(
            "Choose dataset files",
            type=["csv", "json", "parquet"],
            key="dataset_uploader",
            help="Select multiple files (Ctrl+Click or Cmd+Click). Max 10MB per file",
            label_visibility="collapsed",
            accept_multiple_files=True
        )

        # Validate file sizes (10MB = 10 * 1024 * 1024 bytes)
        MAX_FILE_SIZE = 10 * 1024 * 1024
        if dataset_files_uploaded:
            valid_files = []
            for file in dataset_files_uploaded:
                if file.size > MAX_FILE_SIZE:
                    st.error(f"❌ {file.name} exceeds 10MB limit ({file.size / (1024 * 1024):.2f} MB)")
                else:
                    valid_files.append(file)

            if valid_files:
                st.session_state.dataset_files = valid_files
                st.success(f"✓ {len(valid_files)} file(s) uploaded")
                for file in valid_files:
                    st.text(f"  • {file.name} ({file.size / 1024:.1f} KB)")
            else:
                st.session_state.dataset_files = None
        else:
            st.session_state.dataset_files = None

        st.markdown("<br>", unsafe_allow_html=True)

        # Screenshot/Drawing Upload (Required)
        st.markdown("### 2. Dashboard Design <span class='required-star'>*</span>", unsafe_allow_html=True)
        st.markdown("Upload an image showing your desired dashboard/graph layout (screenshot or drawing)")

        screenshot_file = st.file_uploader(
            "Choose an image",
            type=["png", "jpg", "jpeg"],
            key="screenshot_uploader",
            help="Accepted formats: PNG, JPG, JPEG",
            label_visibility="collapsed"
        )

        if screenshot_file:
            st.session_state.screenshot_file = screenshot_file
            # Show thumbnail preview
            image = Image.open(screenshot_file)
            st.image(image, caption="Design Preview", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Additional Information (Optional)
        st.markdown("### 3. Additional Information (Optional)")
        st.markdown("Add any additional context or requirements about your dashboard")

        clarification_text = st.text_area(
            "Clarification",
            value=st.session_state.clarification_text,
            placeholder="e.g., 'Show last 30 days', 'Group by region', 'Use blue color scheme'",
            max_chars=1000,
            height=100,
            label_visibility="collapsed",
            help="Optional: Provide additional context to help us understand your requirements"
        )
        st.session_state.clarification_text = clarification_text

        # Character counter
        char_count = len(clarification_text)
        st.caption(f"{char_count}/1000 characters")

        st.markdown("<br><br>", unsafe_allow_html=True)

        # Upload Button / Progress Bar
        render_upload_button()

        # Footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
                <a href="#" style="margin: 0 1rem;">Help/FAQ</a> |
                <a href="#" style="margin: 0 1rem;">See Examples</a>
            </div>
        """, unsafe_allow_html=True)


def render_upload_button():
    """Render the upload button or progress bar based on upload status"""

    # Check if required fields are filled
    can_upload = (
        st.session_state.dataset_files is not None and
        len(st.session_state.dataset_files) > 0 and
        st.session_state.screenshot_file is not None
    )

    if st.session_state.upload_status == "idle":
        # Show upload button
        if st.button(
            "Upload",
            disabled=not can_upload,
            use_container_width=True,
            type="primary"
        ):
            # Start upload process
            st.session_state.upload_status = "uploading"
            st.session_state.progress = 0
            st.rerun()

        if not can_upload:
            st.caption("⚠️ Please upload both dataset and screenshot to continue")

    elif st.session_state.upload_status in ["uploading", "processing"]:
        # Show progress bar
        render_progress_bar()

    elif st.session_state.upload_status == "complete":
        # Show success and navigate
        st.success("✓ Understanding complete!")
        time.sleep(1)
        navigate_to("chat")

    elif st.session_state.upload_status == "error":
        # Show error
        st.error(f"❌ Upload failed: {st.session_state.get('upload_error', 'Unknown error')}")
        if st.button("Try Again", use_container_width=True):
            st.session_state.upload_status = "idle"
            st.session_state.progress = 0
            st.session_state.upload_error = None
            st.rerun()


def render_progress_bar():
    """Render the animated progress bar with actual API calls"""

    progress = st.session_state.progress

    # Stage 1: Upload and ingest data (0-70%)
    if progress < 70:
        st.session_state.upload_status = "processing"
        stage_text = "Uploading files and ingesting data into DuckDB..."

        # Make API call on first run
        if progress == 0:
            try:
                response = api_client.ingest_data(
                    dataset_files=st.session_state.dataset_files,
                    screenshot_file=st.session_state.screenshot_file,
                    clarification=st.session_state.clarification_text or None
                )
                # Store session ID and metadata
                st.session_state.session_id = response["session_id"]
                st.session_state.metadata = response["tables"]  # List of table metadata
                st.session_state.table_names = [table["table_name"] for table in response["tables"]]
                st.session_state.screenshot_info = response["screenshot_info"]
            except Exception as e:
                st.session_state.upload_status = "error"
                st.session_state.upload_error = str(e)
                st.rerun()
                return

    # Stage 2: Analyze screenshot (70-100%)
    else:
        st.session_state.upload_status = "processing"
        stage_text = "Understanding your requirements..."

        # Make API call at progress 70
        if progress == 70:
            try:
                response = api_client.analyze_screenshot(st.session_state.session_id)
                st.session_state.agent_understanding = response
            except Exception as e:
                st.session_state.upload_status = "error"
                st.session_state.upload_error = str(e)
                st.rerun()
                return

    # Progress bar
    progress_bar = st.progress(progress / 100)

    # Stage text
    st.markdown(f"""
        <div class="progress-stage">{stage_text}</div>
    """, unsafe_allow_html=True)

    # Increment progress
    if progress < 100:
        st.session_state.progress += 10
        time.sleep(0.3)
        st.rerun()
    else:
        st.session_state.upload_status = "complete"
        st.rerun()
