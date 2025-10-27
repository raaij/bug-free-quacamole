# DrawDash: Technical Architecture & Implementation Plan

## System Architecture

DrawDash uses a **multi-agent orchestration** pattern where specialized agents collaborate to transform visual requirements into working dashboards.

## User Input Interface

The frontend provides three input fields:

1. **Dataset Upload** (Required)
   - Upload CSV, JSON or Parquet
   - This is the source data for the dashboard

2. **Visualization Screenshot/Sketch** (Required)
   - Upload an image showing the desired dashboard layout
   - Can be a hand-drawn sketch, mockup, or screenshot of an example

3. **Text Description** (Optional)
   - Additional context or clarifications about the visualization
   - Examples: "Show last 30 days only", "Group by region", "Use blue color scheme"
   - Helps the Vision Agent better understand ambiguous requirements

## Agent Pipeline

### 1. **Data Ingestion Agent**
**Responsibility**: Prepare data for analysis
- Crawl and validate uploaded datasets
- Ingest data into DuckDB for fast analytical queries
- Store metadata about dataset schema and statistics 
- Future: Generate mock data if no dataset is provided (for prototyping)

### 2. **Metadata Store**
**Purpose**: Centralized knowledge base
- Dataset schemas and column types
- Data statistics (ranges, distributions, cardinality)
- Query history and performance metrics
- Visualization mappings and preferences

### 3. **Vision Agent** (Screenshot Understanding)
**Responsibility**: Extract requirements from visual input
- Analyze uploaded screenshots/sketches using vision models (Gemini Vision)
- Parse optional text description for additional context
- Identify chart types (bar, line, pie, scatter, etc.)
- Extract labels, titles, and axis information
- Understand groupings, filters, and aggregations
- Detect layout and dashboard composition

**Output**: Structured JSON specification
```json
{
  "dashboard_title": "Sales Performance Q1",
  "user_notes": "Show last 30 days only",
  "charts": [
    {
      "type": "bar_chart",
      "title": "Revenue by Region",
      "x_axis": "region",
      "y_axis": "revenue",
      "aggregation": "sum",
      "filters": ["date >= '2024-01-01'"]
    }
  ]
}
```

### 4. **SQL Generation Agent**
**Responsibility**: Convert specifications to executable queries
- Take structured JSON from Vision Agent
- Map visualization requirements to SQL queries
- Use metadata store to validate column names and types
- Generate optimized DuckDB-compatible SQL

**Example Transformation**:
- Input: `{"type": "bar_chart", "x_axis": "region", "y_axis": "revenue", "aggregation": "sum"}`
- Output: `SELECT region, SUM(revenue) as revenue FROM dataset GROUP BY region`

### 5. **Query Execution Agent**
**Responsibility**: Execute and validate queries with feedback loop
- Run SQL queries against DuckDB
- Catch and analyze errors (syntax, missing columns, type mismatches)
- Provide feedback to SQL Generation Agent for refinement
- **Iterative loop**: Continue until query executes successfully
- Return validated results to visualization agent

### 6. **Visualization Agent**
**Responsibility**: Generate dashboard code
- Take query results and original specifications
- Generate visualization code (e.g., Plotly, Altair, or custom library)
- Create interactive dashboard layouts
- Apply styling and formatting from screenshot analysis
- Export as standalone HTML/Python/JavaScript

### 7. **Orchestrator Agent** 
**Role**: Coordinate the entire pipeline
- Route tasks between specialized agents
- Handle error recovery and retries
- Track progress and provide status updates
- Manage agent communication and state

## Data Flow

```
User Input:
  - Dataset (CSV/JSON)
  - Screenshot/Sketch
  - Text Description (optional)
    ↓
Data Ingestion Agent → DuckDB + Metadata Store
    ↓
Vision Agent (Screenshot + Text) → Structured JSON Specification
    ↓
SQL Generation Agent → SQL Query
    ↓
Query Execution Agent ↔ SQL Generation Agent (Loop until success)
    ↓
Visualization Agent → Dashboard Code
    ↓
Frontend Display → Interactive Dashboard
```

## Technology Stack

- **Agent Framework**: Google ADK (Gemini 2.5 Flash)
- **Vision Models**: Gemini Vision API (for screenshot analysis)
- **Database**: DuckDB (in-memory analytics)
- **Visualization**: TBD (Plotly, Altair, or custom)
- **Backend**: Python 3.11 with `uv` package manager
- **Frontend**: TBD (potential options: Streamlit, Gradio, React)

## Development Phases

### Phase 1: Core Pipeline (MVP)
- [ ] Set up Data Ingestion Agent with DuckDB integration
- [ ] Implement Vision Agent for screenshot + text analysis
- [ ] Build SQL Generation Agent with basic chart types
- [ ] Create Query Execution Agent with error handling loop
- [ ] Connect agents via Orchestrator

### Phase 2: Visualization & Frontend
- [ ] Implement Visualization Agent
- [ ] Build frontend with 3-input interface (dataset, screenshot, text)
- [ ] Add progress tracking UI

### Phase 3: Enhancement
- [ ] Add mock data generation capability
- [ ] Expand chart type support
- [ ] Improve error recovery mechanisms
- [ ] Add dashboard export functionality

## Success Metrics

- **Speed**: Generate dashboard in < 2 minutes from upload
- **Accuracy**: Vision agent correctly identifies chart types 90%+ of time
- **Reliability**: Query execution succeeds within 3 iterations 95%+ of time
- **Usability**: Non-technical users can create dashboards without code
