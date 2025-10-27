"""Screen 1: Upload Screen - Dataset, Screenshot, and Text inputs"""

import streamlit as st
from PIL import Image
import time
from src.draw_dash.frontend.state import navigate_to


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
        st.markdown("Upload your data file (CSV, JSON, or Parquet)")

        dataset_file = st.file_uploader(
            "Choose a dataset file",
            type=["csv", "json", "parquet"],
            key="dataset_uploader",
            help="Max file size: 10MB",
            label_visibility="collapsed"
        )

        if dataset_file:
            st.session_state.dataset_file = dataset_file
            st.success(f"✓ {dataset_file.name} ({dataset_file.size // 1024} KB)")

        st.markdown("<br>", unsafe_allow_html=True)

        # Screenshot Upload (Required)
        st.markdown("### 2. Screenshot Upload <span class='required-star'>*</span>", unsafe_allow_html=True)
        st.markdown("Upload an image showing your desired dashboard layout")

        screenshot_file = st.file_uploader(
            "Choose a screenshot",
            type=["png", "jpg", "jpeg"],
            key="screenshot_uploader",
            help="Accepted formats: PNG, JPG, JPEG",
            label_visibility="collapsed"
        )

        if screenshot_file:
            st.session_state.screenshot_file = screenshot_file
            # Show thumbnail preview
            image = Image.open(screenshot_file)
            st.image(image, caption="Screenshot Preview", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Clarification Text (Optional)
        st.markdown("### 3. Clarification Text (Optional)")
        st.markdown("Add any clarifications about your dashboard")

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
        st.session_state.dataset_file is not None and
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


def render_progress_bar():
    """Render the animated progress bar"""

    # Simulate progress
    if st.session_state.progress < 50:
        st.session_state.upload_status = "uploading"
        stage_text = "Uploading data to DuckDB..."
    else:
        st.session_state.upload_status = "processing"
        stage_text = "Understanding your requirements..."

    # Progress bar
    progress_bar = st.progress(st.session_state.progress / 100)

    # Stage text
    st.markdown(f"""
        <div class="progress-stage">{stage_text}</div>
    """, unsafe_allow_html=True)

    # Increment progress
    if st.session_state.progress < 100:
        st.session_state.progress += 10
        time.sleep(0.3)
        st.rerun()
    else:
        st.session_state.upload_status = "complete"
        st.rerun()