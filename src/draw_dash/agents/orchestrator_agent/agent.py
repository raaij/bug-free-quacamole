from google.adk.agents import SequentialAgent

from draw_dash.agents.vision_agent.agent import root_agent as vision_agent
from draw_dash.agents.query_generator_agent.agent import root_agent as query_generator_agent
from draw_dash.agents.query_execution_agent.agent import root_agent as query_execution_agent

root_agent = SequentialAgent(
    name="orchestrator_agent",
    description="Orchestrates the complete workflow from sketch analysis to query execution",
    sub_agents=[
        vision_agent,
        query_generator_agent,
        query_execution_agent,
    ],
)
