from google.adk.agents import Agent

root_agent = Agent(
   name="orchestrator_agent",
   model="gemini-2.5-flash",
   description="Orchestrator agent.",
   instruction="You are a helpful assistant."
)
