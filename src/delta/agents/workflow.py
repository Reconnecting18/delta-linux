"""Workflow agent.

This agent coordinates multi-step plans and delegates work to specialist agents.
"""

from __future__ import annotations

from delta.agents._ollama import generate
from delta.agents.base import Agent

_SYSTEM_PROMPT = (
    "You are deltai, a helpful Linux AI assistant. "
    "Answer the user's request clearly and concisely. "
    "For multi-step tasks, break them down and guide the user step by step."
)


class WorkflowAgent(Agent):
    """Default coordinator for general or mixed-intent requests."""

    name = "workflow"

    async def run(self, query: str, source: str, session_id: str | None = None) -> str:
        return await generate(self.settings, query, system=_SYSTEM_PROMPT)
