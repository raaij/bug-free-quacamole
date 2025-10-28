from google.adk.agents import LoopAgent, SequentialAgent
from google.adk.tools.tool_context import ToolContext

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from draw_dash.agents.query_generator_agent.agent import root_agent as query_generator_agent
from draw_dash.agents.query_execution_agent.agent import root_agent as query_execution_agent


query_retry_loop = LoopAgent(
    name="QueryRetryLoop", 
    sub_agents=[
        query_generator_agent,
        query_execution_agent,
    ],
    max_iterations=5
)

root_agent = SequentialAgent(
    name="QueryLoopPipeline",
    sub_agents=[
        query_retry_loop
    ],
    description="Generates SQL queries and executes them with automatic error correction and retry logic."
)