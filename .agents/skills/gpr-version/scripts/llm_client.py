from __future__ import annotations

import os
from dataclasses import dataclass
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@dataclass
class LLMConfig:
    base_url: str | None
    api_key: str | None
    model: str

def cfg() -> LLMConfig:
    return LLMConfig(
        base_url=os.environ.get("LLM_BASE_URL"),
        api_key=os.environ.get("LLM_API_KEY"),
        model=os.environ.get("LLM_MODEL", "gpt-4.1-mini"),
    )

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, min=0.5, max=4))
async def chat(messages: list[dict], *, temperature: float = 0.2) -> str:
    c = cfg()
    if not c.base_url or not c.api_key:
        raise RuntimeError("LLM not configured")

    url = c.base_url.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {c.api_key}"}
    payload = {"model": c.model, "messages": messages, "temperature": temperature}

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
