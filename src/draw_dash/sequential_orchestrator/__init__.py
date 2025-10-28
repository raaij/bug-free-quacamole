"""
Sequential Orchestrator

Chains VisionAgent → QueryGenerator in strict sequential order.
"""

from .agent import root_agent

__all__ = ["root_agent"]