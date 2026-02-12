from __future__ import annotations

import os

try:
    from google import genai
except Exception:  # pragma: no cover
    import google.genai as genai  # type: ignore

from google.genai import types


class LLMUnavailable(RuntimeError):
    pass


def _require_key() -> None:
    if not os.getenv("GEMINI_API_KEY"):
        raise LLMUnavailable("GEMINI_API_KEY is not configured")


def generate_text(prompt: str, *, thinking_level: str = "minimal") -> str:
    _require_key()
    model = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
    level = os.getenv("GEMINI_THINKING_LEVEL", thinking_level)

    try:
        client = genai.Client()
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level=level)
            ),
        )
        if not response.text:
            raise LLMUnavailable("Gemini returned empty response")
        return response.text
    except LLMUnavailable:
        raise
    except Exception as exc:
        raise LLMUnavailable(f"Gemini request failed: {exc}") from exc
