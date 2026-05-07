"""Shell agent.

This agent handles Linux shell and command-line task requests.
"""

from __future__ import annotations

from delta.agents._ollama import generate
from delta.agents.base import Agent

_SYSTEM_PROMPT = (
    "You are a Linux shell expert. "
    "When given a task, respond with the exact bash or sh commands needed, "
    "preceded by a brief explanation of what each command does. "
    "Prefer safe, non-destructive commands. "
    "If a command could be dangerous, warn the user clearly before showing it."
)


class ShellAgent(Agent):
    """Handles shell and command-line task execution requests."""

    name = "shell"

    async def run(self, query: str, source: str, session_id: str | None = None) -> str:
        return await generate(self.settings, query, system=_SYSTEM_PROMPT)
