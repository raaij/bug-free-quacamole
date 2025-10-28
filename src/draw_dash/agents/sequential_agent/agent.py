from google.adk.agents import SequentialAgent

from draw_dash.agents.data_agent.agent import root_agent as data_agent
from draw_dash.agents.json_extractor_agent.agent import root_agent as json_extractor_agent
from draw_dash.agents.query_generator_agent.agent import root_agent as query_generator_agent
from draw_dash.agents.dash_agent.agent import root_agent as dash_agent

root_agent = SequentialAgent(
    name="sequential_agent",
    description="Orchestrates the complete workflow from sketch analysis to query execution",
    sub_agents=[
        data_agent,
        json_extractor_agent,
        query_generator_agent,
        dash_agent,
    ],
)
