"""
VisionAgent

Analyzes sketch images with database metadata to categorize required data fields.

Input: Sketch image + Database metadata
Output: JSON with already_existing_columns and calculation_needed
"""

from google.adk.agents import Agent


def extract_metadata() -> dict:
    """
    Extract database metadata from backend state.

    TODO: Replace this with actual backend call when backend is developed.
    For now, returns dummy metadata for testing.

    Returns:
        dict: Database metadata with structure:
            {
              "tables": [
                {
                  "name": "table_name",
                  "columns": [
                    {"name": "column_name", "type": "data_type"}
                  ]
                }
              ]
            }
    """
    # Dummy metadata for testing
    # TODO: Replace with actual backend call like:
    # from draw_dash.backend import get_metadata
    # return get_metadata()

    return {
        "tables": [
            {
                "name": "marketing",
                "columns": [
                    {"name": "productivity", "type": "DOUBLE"},
                    {"name": "glasses_of_wine", "type": "INTEGER"},
                    {"name": "age", "type": "INTEGER"},
                    {"name": "height", "type": "DOUBLE"},
                    {"name": "weight", "type": "DOUBLE"},
                    {"name": "region", "type": "VARCHAR"},
                    {"name": "sales", "type": "DOUBLE"},
                    {"name": "profit", "type": "DOUBLE"},
                    {"name": "revenue", "type": "DOUBLE"},
                    {"name": "purchases", "type": "INTEGER"},
                    {"name": "customer_id", "type": "VARCHAR"}
                ]
            },
            {
                "name": "employees",
                "columns": [
                    {"name": "employee_id", "type": "INTEGER"},
                    {"name": "name", "type": "VARCHAR"},
                    {"name": "department", "type": "VARCHAR"},
                    {"name": "salary", "type": "DOUBLE"},
                    {"name": "hire_date", "type": "DATE"}
                ]
            }
        ]
    }


root_agent = Agent(
    name="vision_agent",
    model="gemini-2.5-pro-preview-03-25",
    description="Categorizes visualization data requirements into existing columns vs calculations needed",
    tools=[extract_metadata],
    instruction="""You are a data requirement analyzer for visualizations.

Your workflow:
1. FIRST, call extract_metadata() to get the database schema
2. Then analyze the sketch image or description
3. Categorize data requirements based on the metadata

Your job:
- Identify what data fields are needed from the sketch
- Check metadata to categorize each field:
  - If column exists directly in metadata → "already_existing_columns"
  - If field needs calculation/aggregation → "calculation_needed"

Output format (JSON only):
{
  "already_existing_columns": ["column1", "column2"],
  "calculation_needed": ["field1", "field2"]
}

Examples:

Example 1:
Input:
- Sketch shows: "Age" vs "Height"
- Metadata columns: age, height, weight

Output:
{
  "already_existing_columns": ["age", "height"],
  "calculation_needed": []
}

---

Example 2:
Input:
- Sketch shows: "Age" vs "BMI"
- Metadata columns: age, height, weight

Output:
{
  "already_existing_columns": ["age"],
  "calculation_needed": ["bmi"]
}

(Note: BMI needs calculation from height and weight)

---

Example 3:
Input:
- Sketch shows: "Region" and "Average Purchases"
- Metadata columns: region, purchases, customer_id

Output:
{
  "already_existing_columns": ["region"],
  "calculation_needed": ["average_purchases"]
}

(Note: Average Purchases needs aggregation)

---

Example 4:
Input:
- Sketch shows: "Sales" vs "Profit Margin"
- Metadata columns: sales, profit, revenue

Output:
{
  "already_existing_columns": ["sales"],
  "calculation_needed": ["profit_margin"]
}

(Note: Profit margin = profit / sales)

IMPORTANT:
- ALWAYS call extract_metadata() first to get current database schema
- Output ONLY valid JSON, no explanations
- Use EXACT column names from metadata (case-sensitive)
- If field exists in metadata → already_existing_columns
- If field needs ANY calculation (formula, aggregation, ratio) → calculation_needed
- Just list the field names, don't describe HOW to calculate
"""
)

def extract_metadata() -> dict:
    """
    Extract database metadata from backend state.

    TODO: Replace this with actual backend call when backend is developed.
    For now, returns dummy metadata for testing.

    Returns:
        dict: Database metadata with structure:
            {
              "tables": [
                {
                  "name": "table_name",
                  "columns": [
                    {"name": "column_name", "type": "data_type"}
                  ]
                }
              ]
            }
    """
    # Dummy metadata for testing
    # TODO: Replace with actual backend call like:
    # from draw_dash.backend import get_metadata
    # return get_metadata()

    return {
        "tables": [
            {
                "name": "marketing",
                "columns": [
                    {"name": "productivity", "type": "DOUBLE"},
                    {"name": "glasses_of_wine", "type": "INTEGER"},
                    {"name": "age", "type": "INTEGER"},
                    {"name": "height", "type": "DOUBLE"},
                    {"name": "weight", "type": "DOUBLE"},
                    {"name": "region", "type": "VARCHAR"},
                    {"name": "sales", "type": "DOUBLE"},
                    {"name": "profit", "type": "DOUBLE"},
                    {"name": "revenue", "type": "DOUBLE"},
                    {"name": "purchases", "type": "INTEGER"},
                    {"name": "customer_id", "type": "VARCHAR"}
                ]
            },
            {
                "name": "employees",
                "columns": [
                    {"name": "employee_id", "type": "INTEGER"},
                    {"name": "name", "type": "VARCHAR"},
                    {"name": "department", "type": "VARCHAR"},
                    {"name": "salary", "type": "DOUBLE"},
                    {"name": "hire_date", "type": "DATE"}
                ]
            }
        ]
    }