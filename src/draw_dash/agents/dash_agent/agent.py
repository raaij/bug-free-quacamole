"""
VisionAgent

Analyzes sketch images with database metadata to categorize required data fields.

Input: Sketch image + Database metadata
Output: JSON with already_existing_columns and calculation_needed
"""

from google.adk.agents import Agent

from draw_dash.constant import PATH_DRAW_DASH
from draw_dash.tool.dashboard import read_dashboard_code, modify_dashboard_code

with open(PATH_DRAW_DASH / "tool" / "read_data.py") as fp:
    content = fp.read()

root_agent = Agent(
    name="dash_agent",
    model="gemini-2.5-pro-preview-03-25",
    description="Creates a dashboard.",
    instruction=("""
Provided the following table metadata:
<metadata>
{table_information}
</metadata>

Together with dashboard spec:
<spec>
{dash_json}
</spec>

And queries:
<queries>
{all_query}
</queries>

Please modify the dashboard code to show the charts with the queries created.

The dashboard code uses streamlit.

For any queries use DuckDB. You can import duckdb in the dashboard code.
"""),
    tools=[read_dashboard_code, modify_dashboard_code],
)