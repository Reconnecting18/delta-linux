"""Shared Ollama client used by daemon agents.

Each agent calls into Ollama with an intent-specific system prompt; this
module centralizes the HTTP call, timeout, and error mapping so individual
agent files stay small.
"""

from __future__ import annotations

import httpx

from delta.config import Settings


async def generate(settings: Settings, prompt: str, system: str | None = None) -> str:
    """Call Ollama /api/generate and return the response text.

    Returns a user-facing error string instead of raising, so agents can
    forward the result directly to the orchestrator.
    """
    model = settings.ollama_fast_model
    url = settings.ollama_url.rstrip("/") + "/api/generate"
    payload: dict[str, object] = {"model": model, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json().get("response", "").strip() or "No response from model."
    except httpx.ConnectError:
        return "Cannot connect to Ollama. Make sure it's running (ollama serve)."
    except Exception as exc:
        return f"Model error: {type(exc).__name__}"
