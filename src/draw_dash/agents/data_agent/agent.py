from google.adk.agents import Agent

from draw_dash.tool.read_data import (
    ingest_file,
    read_data_files,
    get_table_list,
    get_table_metadata,
)

root_agent = Agent(
    name="data_agent",
    model="gemini-2.5-pro-preview-03-25",
    description="Initialises data.",
    instruction="""
You set up a DuckDB database based on the data provided.

Please use the `read_data_files` tool to see what data is available.

You can then use `ingest_file` to ingest the file into DuckDB.

Your output should be a list of the tables you have created, together with some metadata information. You can create
this with the information from `get_table_list`, and `get_table_metadata`
""",
    tools=[
        read_data_files,
        ingest_file,
    ],
    output_key="table_information"
)
