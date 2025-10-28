"""
Sequential Orchestrator Agent

Coordinates the pipeline: VisionAgent → QueryGenerator
"""

from google.adk.agents import SequentialAgent
from draw_dash.vision_agent.agent import root_agent as vision_agent
from draw_dash.query_generator_agent.agent import root_agent as query_generator_agent

sequential_orchestrator = SequentialAgent(
    name="sequential_orchestrator",
    sub_agents=[vision_agent, query_generator_agent],
    description="Executes VisionAgent then QueryGenerator in sequence for SQL generation from sketches",
)

root_agent = sequential_orchestrator