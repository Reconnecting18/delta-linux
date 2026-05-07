"""File agent.

This agent handles file system navigation, search, and editing tasks.
"""

from __future__ import annotations

from delta.agents._ollama import generate
from delta.agents.base import Agent

_SYSTEM_PROMPT = (
    "You are a Linux filesystem expert. "
    "Help the user navigate, search, read, and edit files safely. "
    "Provide exact commands (ls, find, grep, cat, cp, mv, etc.) with clear explanations. "
    "Always warn before suggesting commands that modify or delete files. "
    "Use XDG base directories (~/.local, ~/.config, ~/.cache) when appropriate."
)


class FileAgent(Agent):
    """Handles file navigation and editing tasks."""

    name = "file"

    async def run(self, query: str, source: str, session_id: str | None = None) -> str:
        return await generate(self.settings, query, system=_SYSTEM_PROMPT)
