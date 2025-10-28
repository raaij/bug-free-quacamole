from google.adk.agents import Agent

from draw_dash.tool import execute_query, diagnose_sql_error, format_diagnosis_for_agent
from google.adk.tools import ToolContext


def exit_loop(tool_context: ToolContext):
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    return {}


root_agent = Agent(
    name="query_execution_agent",
    model="gemini-2.5-pro-preview-03-25",
    description="Executes SQL queries and manages retry loop termination based on execution success or failure.",
    output_key="execution_result",
    instruction="""You execute SQL queries using provided inputs and coordinate loop termination.

INPUTS:
- SQL Query: {generated_query}

TASK:
Execute the SQL query and handle the result based on success or failure.

EXECUTION LOGIC:
1. Execute the SQL query using execute_query tool
2. Check the result type:

   IF RESULT IS A DATAFRAME (success):
   - IMMEDIATELY call exit_loop tool
   - Output confirmation message
   - Job finished

   IF RESULT IS ERROR STRING (failure):
   - Output the complete error message
   - Do NOT call exit_loop
   - Continue to next iteration

DECISION CRITERIA:
- SUCCESS = Result is a JSON string (starts with '[' and contains data)
- FAILURE = Result is an error string"

The successful SQL results will be returned as the final output to the next agent in the pipeline.
""",
    tools=[execute_query, diagnose_sql_error, format_diagnosis_for_agent, exit_loop],
)
