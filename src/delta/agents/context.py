"""Context agent.

This agent gathers and summarizes system context for other agents.
"""

from __future__ import annotations

from delta.agents._ollama import generate
from delta.agents.base import Agent

_SYSTEM_PROMPT = (
    "You are a desktop context analyst for a Linux system. "
    "Help the user understand their current system state: active applications, "
    "clipboard contents, environment variables, running processes, and workspace layout. "
    "Suggest how to use context information effectively. "
    "Be concise and practical."
)


class ContextAgent(Agent):
    """Handles contextual data gathering and summarization."""

    name = "context"

    async def run(self, query: str, source: str, session_id: str | None = None) -> str:
        return await generate(self.settings, query, system=_SYSTEM_PROMPT)
