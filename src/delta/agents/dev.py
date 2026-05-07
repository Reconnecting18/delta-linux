"""Developer agent.

This agent handles coding workflows, code review, tests, and refactoring.
"""

from __future__ import annotations

from delta.agents._ollama import generate
from delta.agents.base import Agent

_SYSTEM_PROMPT = (
    "You are a senior software engineer with deep Linux and Python expertise. "
    "Help with coding tasks: writing code, debugging, refactoring, tests, and code review. "
    "Provide complete, working code snippets with brief explanations. "
    "Prefer clean, idiomatic solutions. "
    "If reviewing code, point out bugs, security issues, and improvement opportunities."
)


class DevAgent(Agent):
    """Handles development-centric tasks."""

    name = "dev"

    async def run(self, query: str, source: str, session_id: str | None = None) -> str:
        return await generate(self.settings, query, system=_SYSTEM_PROMPT)
