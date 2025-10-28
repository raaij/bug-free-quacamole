"""API Client for communicating with DrawDash backend"""

import requests
from typing import Optional, Dict, Any
import streamlit as st

# Backend API URL
API_BASE_URL = "http://localhost:8000"


class APIClient:
    """Client for DrawDash backend API"""

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url

    def ingest_data(
        self,
        dataset_files: list,
        screenshot_file,
        clarification: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Unified method: Upload files and ingest data into DuckDB

        Args:
            dataset_files: List of UploadedFile objects for datasets
            screenshot_file: UploadedFile object for screenshot
            clarification: Optional clarification text

        Returns:
            Response dict with session_id, table metadata, and screenshot info
        """
        url = f"{self.base_url}/api/ingest"

        # Reset file pointers to beginning
        screenshot_file.seek(0)

        # Prepare multipart form data with multiple dataset files
        files = []
        for dataset_file in dataset_files:
            dataset_file.seek(0)
            files.append(('datasets', (dataset_file.name, dataset_file, dataset_file.type)))

        # Add screenshot
        files.append(('screenshot', (screenshot_file.name, screenshot_file, screenshot_file.type)))

        data = {}
        if clarification:
            data['clarification'] = clarification

        try:
            response = requests.post(url, files=files, data=data, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to ingest data: {str(e)}")

    def analyze_screenshot(self, session_id: str) -> Dict[str, Any]:
        """
        Analyze screenshot using Vision Agent

        Args:
            session_id: Session identifier

        Returns:
            Response dict with agent understanding
        """
        url = f"{self.base_url}/api/analyze/{session_id}"

        try:
            response = requests.post(url, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to analyze screenshot: {str(e)}")


# Singleton instance
api_client = APIClient()