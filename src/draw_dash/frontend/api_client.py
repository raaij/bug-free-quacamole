"""API Client for communicating with DrawDash backend"""

import requests
from typing import Optional, Dict, Any
import streamlit as st

# Backend API URL
API_BASE_URL = "http://localhost:8080"
ADK_API_BASE_URL = "http://localhost:8000"


class APIClient:
    """Client for DrawDash backend API"""

    def __init__(self, base_url: str = API_BASE_URL, adk_base_url: str = ADK_API_BASE_URL):
        self.base_url = base_url
        self.adk_base_url = adk_base_url

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

    def call_vision_agent(
        self,
        screenshot_bytes: bytes,
        screenshot_filename: str,
        database_metadata: Dict[str, Any],
        user_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call the vision_agent through ADK API server

        Args:
            screenshot_bytes: Screenshot image file bytes
            screenshot_filename: Name of screenshot file
            database_metadata: Database schema information (tables, columns, types)
            user_notes: Optional user clarification text

        Returns:
            Dict with 'already_existing_columns' and 'calculation_needed' lists
        """
        # Create a session for the vision agent
        session_id = f"vision_session_{hash(screenshot_filename)}"
        user_id = "frontend_user"

        # First, create/update the session
        session_url = f"{self.adk_base_url}/apps/vision_agent/users/{user_id}/sessions/{session_id}"
        try:
            requests.post(session_url, json={"state": {}}, timeout=10)
        except:
            pass  # Session creation is optional

        # Prepare the message with image and metadata
        import base64
        image_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')

        # Construct the prompt with better formatting
        def format_metadata_for_agent(metadata):
            """Format database metadata in a structured way for agent consumption"""
            if not metadata or not metadata.get('tables'):
                return "No database metadata available."

            formatted = "DATABASE SCHEMA:\n"
            for table in metadata.get('tables', []):
                formatted += f"\nTable: {table.get('table_name')} ({table.get('row_count', 0)} rows)\n"
                formatted += "Columns:\n"

                for col in table.get('columns', []):
                    col_info = f"  - {col.get('name')} ({col.get('type', 'unknown')})"

                    # Add statistics if available
                    stats = table.get('column_stats', {}).get(col.get('name'), {})
                    if stats:
                        stat_parts = []
                        if 'min' in stats and stats['min'] is not None:
                            stat_parts.append(f"min: {stats['min']}")
                        if 'max' in stats and stats['max'] is not None:
                            stat_parts.append(f"max: {stats['max']}")
                        if 'avg' in stats and stats['avg'] is not None:
                            stat_parts.append(f"avg: {stats['avg']:.2f}")
                        if 'distinct_count' in stats:
                            stat_parts.append(f"distinct: {stats['distinct_count']}")

                        if stat_parts:
                            col_info += f" [{', '.join(stat_parts)}]"

                    formatted += col_info + "\n"

            return formatted

        prompt_text = f"""{format_metadata_for_agent(database_metadata)}

"""
        if user_notes:
            prompt_text += f"User Notes: {user_notes}\n\n"

        prompt_text += "Please analyze the sketch image and categorize the data requirements."

        message = {
            "role": "user",
            "parts": [
                {
                    "inline_data": {
                        "mime_type": "image/png" if screenshot_filename.lower().endswith('.png') else "image/jpeg",
                        "data": image_base64
                    }
                },
                {"text": prompt_text}
            ]
        }

        # Call the ADK /run endpoint
        run_url = f"{self.adk_base_url}/run"
        payload = {
            "app_name": "vision_agent",
            "user_id": user_id,
            "session_id": session_id,
            "new_message": message
        }

        try:
            response = requests.post(run_url, json=payload, timeout=60)
            response.raise_for_status()
            events = response.json()

            # Extract the agent's response from events
            # The response is an array of events with structure: [{content: {parts: [{text: "..."}], role: "model"}, ...}]
            for event in events:
                if event.get("content") and event["content"].get("parts"):
                    for part in event["content"]["parts"]:
                        if "text" in part:
                            agent_text = part["text"]
                            # Parse JSON from agent's response
                            import json
                            try:
                                # First try direct JSON parsing
                                result = json.loads(agent_text)
                                return result
                            except json.JSONDecodeError:
                                # Try to extract JSON from markdown code blocks
                                if "```json" in agent_text:
                                    json_start = agent_text.find("```json") + 7
                                    json_end = agent_text.find("```", json_start)
                                    json_text = agent_text[json_start:json_end].strip()
                                    return json.loads(json_text)
                                elif "```" in agent_text:
                                    # Try generic code block
                                    json_start = agent_text.find("```") + 3
                                    json_end = agent_text.find("```", json_start)
                                    json_text = agent_text[json_start:json_end].strip()
                                    return json.loads(json_text)
                                raise Exception(f"Could not parse agent response as JSON: {agent_text}")

            raise Exception("No agent response found in events")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to call vision agent: {str(e)}")


# Singleton instance
api_client = APIClient()