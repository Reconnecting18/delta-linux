"""Workflow agent.

This agent coordinates multi-step plans and delegates work to specialist agents.
"""

from __future__ import annotations

import httpx

from delta.agents.base import Agent


class WorkflowAgent(Agent):
    """Default coordinator for general or mixed-intent requests."""

    name = "workflow"

    async def run(self, query: str, source: str, session_id: str | None = None) -> str:
        model = self.settings.ollama_fast_model
        url = self.settings.ollama_url.rstrip("/") + "/api/generate"
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(
                    url, json={"model": model, "prompt": query, "stream": False}
                )
                resp.raise_for_status()
                return resp.json().get("response", "").strip() or "No response from model."
        except httpx.ConnectError:
            return "Cannot connect to Ollama. Make sure it's running (ollama serve)."
        except Exception as exc:
            return f"Model error: {type(exc).__name__}"
