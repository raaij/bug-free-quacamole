"""
DrawDash Backend API
FastAPI server for handling agent orchestration and data processing
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import tempfile
import shutil
from pathlib import Path
from src.draw_dash.duckdb_manager import db_manager

# Initialize FastAPI app
app = FastAPI(
    title="DrawDash API",
    description="AI-powered dashboard generation from screenshots",
    version="0.1.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Pydantic Models
# ============================================================================

class IngestResponse(BaseModel):
    """Response after ingesting data"""
    session_id: str
    tables: List[Dict[str, Any]]  # List of table metadata
    screenshot_info: Dict[str, Any]
    message: str
    clarification: Optional[str] = None


class AgentUnderstanding(BaseModel):
    """Agent's understanding of the requirements"""
    dashboard_title: str
    visualizations: List[Dict[str, Any]]
    filters: List[str]
    additional_notes: Optional[str] = None
    confidence: float


# ============================================================================
# App State Storage
# ============================================================================

# Initialize app state on startup
@app.on_event("startup")
async def startup_event():
    """Initialize application state"""
    app.state.sessions = {}  # session_id -> session metadata


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "DrawDash API is running",
        "version": "0.1.0"
    }


@app.post("/api/ingest", response_model=IngestResponse)
async def ingest_data(
    datasets: List[UploadFile] = File(...),
    screenshot: UploadFile = File(...),
    clarification: Optional[str] = Form(None)
):
    """
    Unified endpoint: Upload files and ingest data into DuckDB

    This endpoint:
    1. Accepts multiple dataset files and a screenshot
    2. Validates file types and sizes
    3. Saves files temporarily
    4. Ingests each dataset into DuckDB as a separate table
    5. Stores metadata in app.state

    Args:
        datasets: List of CSV, JSON, or Parquet files (max 10MB each)
        screenshot: PNG, JPG, or JPEG image
        clarification: Optional text description

    Returns:
        IngestResponse with session ID, table metadata, and screenshot info
    """
    import uuid
    import re

    # Validate file types
    allowed_dataset_types = ["text/csv", "application/json", "application/octet-stream"]
    allowed_image_types = ["image/png", "image/jpeg"]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    # Validate all dataset files
    for dataset in datasets:
        if dataset.content_type not in allowed_dataset_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid dataset type for {dataset.filename}. Allowed: CSV, JSON, Parquet"
            )
        if dataset.size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"{dataset.filename} exceeds 10MB limit ({dataset.size / (1024 * 1024):.2f} MB)"
            )

    if screenshot.content_type not in allowed_image_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image type. Allowed: PNG, JPG, JPEG"
        )

    # Generate session ID
    session_id = str(uuid.uuid4())

    # Save files temporarily
    temp_dir = Path(tempfile.gettempdir()) / "drawdash" / session_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Save screenshot
    screenshot_path = temp_dir / screenshot.filename
    with screenshot_path.open("wb") as buffer:
        shutil.copyfileobj(screenshot.file, buffer)

    screenshot_info = {
        "filename": screenshot.filename,
        "size": screenshot.size,
        "type": screenshot.content_type,
        "path": str(screenshot_path)
    }

    # Process and ingest all datasets
    tables_metadata = []

    try:
        for idx, dataset in enumerate(datasets):
            # Save dataset file
            dataset_path = temp_dir / dataset.filename
            with dataset_path.open("wb") as buffer:
                shutil.copyfileobj(dataset.file, buffer)

            # Create unique table name
            filename = Path(dataset.filename).stem
            # Remove all non-alphanumeric characters except underscores
            safe_filename = re.sub(r'[^a-zA-Z0-9_]', '_', filename)
            # Ensure it starts with a letter or underscore
            if safe_filename and safe_filename[0].isdigit():
                safe_filename = f"table_{safe_filename}"
            table_name = f"{safe_filename}_{session_id.replace('-', '_')}"

            # Ingest file into DuckDB and get metadata
            metadata = db_manager.ingest_file(
                file_path=str(dataset_path),
                table_name=table_name
            )

            # Add original filename to metadata
            metadata["original_filename"] = dataset.filename
            metadata["file_size"] = dataset.size

            tables_metadata.append(metadata)

    except Exception as e:
        # Clean up temp files on error
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest data: {str(e)}"
        )

    # Store metadata in app.state
    app.state.sessions[session_id] = {
        "tables": tables_metadata,
        "screenshot_info": screenshot_info,
        "clarification": clarification,
        "temp_dir": str(temp_dir),
        "status": "ingested"
    }

    return IngestResponse(
        session_id=session_id,
        tables=tables_metadata,
        screenshot_info=screenshot_info,
        message=f"{len(datasets)} dataset(s) ingested into DuckDB",
        clarification=clarification
    )


@app.post("/api/analyze/{session_id}", response_model=AgentUnderstanding)
async def analyze_screenshot(session_id: str):
    """
    Analyze screenshot using Vision Agent

    Args:
        session_id: Session identifier

    Returns:
        Agent's understanding of the requirements
    """

    if session_id not in app.state.sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = app.state.sessions[session_id]

    # TODO: Implement Vision Agent
    # - Analyze screenshot with Gemini Vision
    # - Parse clarification text
    # - Extract chart types, labels, filters
    # - Generate structured JSON

    # Mock response for now
    understanding = AgentUnderstanding(
        dashboard_title="Sales Performance Dashboard",
        visualizations=[
            {
                "type": "bar_chart",
                "title": "Revenue by Region",
                "x_axis": "region",
                "y_axis": "revenue",
                "aggregation": "sum"
            },
            {
                "type": "line_chart",
                "title": "Sales Trend Over Time",
                "x_axis": "date",
                "y_axis": "sales",
                "time_range": "last_30_days"
            }
        ],
        filters=["date >= '2024-01-01'"],
        additional_notes=session.get("clarification"),
        confidence=0.85
    )

    session["understanding"] = understanding.dict()
    session["status"] = "analyzed"

    return understanding




# ============================================================================
# Server startup
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)