# Coding/Debugging Sub-Agents Architecture

This project consists of three specialized sub-agents for managing different aspects of the application:

## 1. Frontend Agent (`streamlit-frontend-runner`)

**Purpose**: Manages the Streamlit frontend server

**Responsibilities**:
- Starting and monitoring the Streamlit frontend server
- Handling frontend-related issues and diagnostics
- Monitoring frontend server logs for errors and warnings
- Restarting the frontend when code changes are made

**Use Cases**:
- User requests to start/restart the frontend
- Frontend UI updates and changes need to be viewed
- Frontend errors need to be diagnosed
- Proactive testing after frontend code modifications

## 2. Backend DuckDB Service Agent (`fastapi-backend-runner`)

**Purpose**: Manages the FastAPI backend that exposes DuckDB functionality

**Responsibilities**:
- Creating, configuring, and launching FastAPI applications
- Running existing FastAPI servers that expose DuckDB
- Monitoring FastAPI server logs in real-time
- Troubleshooting startup and runtime issues
- Managing server lifecycle (start/stop/restart)
- Debugging API endpoint errors

**Use Cases**:
- Setting up new FastAPI servers for database access
- Exposing DuckDB through REST endpoints
- Monitoring database query performance
- Handling API authentication and middleware configuration
- Real-time log monitoring for database operations

## 3. ADK Backend Specialist Agent (`adk-backend-specialist`)

**Purpose**: Manages Google's Agent Development Kit (ADK) backend for agent systems

**Responsibilities**:
- Creating and modifying ADK agent configurations
- Exposing agents through API endpoints
- Implementing agent testing strategies
- Debugging ADK CLI commands
- Interpreting ADK application logs
- Multi-agent architecture design and orchestration

**Use Cases**:
- Developing multi-agent backend systems
- Setting up agent API endpoints
- Writing and running agent tests
- Analyzing agent logs and debugging issues
- Managing agent-to-agent communication

## Agent Coordination

These three agents work together to provide a full-stack application:

1. **Frontend Layer**: Streamlit UI for user interaction
2. **Data Layer**: FastAPI + DuckDB for data operations
3. **Intelligence Layer**: ADK agents for complex business logic and orchestration

Each agent can be invoked independently based on the task at hand, and they can work in parallel when changes span multiple layers.