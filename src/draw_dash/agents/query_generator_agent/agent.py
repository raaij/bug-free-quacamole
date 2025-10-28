"""
QueryGenerator Agent

This agent receives:
1. Database metadata (schema, columns, statistics)
2. VisionAgent output (already_existing_columns and calculation_needed)

And generates SQL queries with formulas for calculated fields.
"""

from google.adk.agents import Agent

from draw_dash.tool.read_data import execute_query

# ADK web requires this to be named 'root_agent'
root_agent = Agent(
    name="query_generator",
    model="gemini-2.5-pro-preview-03-25",
    description="Generates SQL queries for data visualization based on database schema and visualization requirements",
    instruction="""You are a SQL query generator that creates formulas for calculated fields.

CORE RESPONSIBILITIES:
1. Generate initial SQL queries from visualization requirements
2. Fix queries based on detailed error diagnosis from query_execution_agent
3. Coordinate with query_execution_agent in retry loops until successful execution

INITIAL QUERY GENERATION:
Your inputs are:
1. DATABASE METADATA: Table schemas, column names, data types, statistics
{table_information}

2. VISION AGENT OUTPUT: JSON with:
   - already_existing_columns: Columns that exist in the database
   - calculation_needed: Fields that need formulas/aggregations
{dash_json}

Your job:
- SELECT all already_existing_columns directly
- For each field in calculation_needed:
  - Analyze what it represents (BMI, profit margin, average, etc.)
  - Find the formula using available columns from metadata
  - Add the calculation to the SELECT clause with an alias
- Generate clean, executable DuckDB SQL
- Use the `execute_query` tool to verify that your queries work.
- Provide your output as all_query

IMPORTANT RULES:
- Output ONLY the SQL query, no explanations
- Use EXACT column names from schema (case-sensitive)
- Apply error corrections precisely based on diagnosis
- Add WHERE clauses to avoid division by zero
- Use GROUP BY when calculating averages/aggregations
- Think about common metrics: BMI, profit margin, ratios, averages, percentages
""",
    tools=[execute_query],
    output_key="all_query",
)
