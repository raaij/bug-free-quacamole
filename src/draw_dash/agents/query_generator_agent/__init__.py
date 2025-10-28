"""
QueryGenerator Agent

This agent converts visualization specifications to SQL queries.
It understands database metadata and generates appropriate queries
for data visualization needs.
"""

from .agent import root_agent

__all__ = ["root_agent"]