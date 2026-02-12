# Demo steps

## AI fallback mode (bez Gemini klíče)
1. Ujisti se, že `GEMINI_API_KEY` není nastavený.
2. Spusť `POST /api/agent/run?incident_id=<uuid>&mode=both`.
3. V `/audit` ověř `action=agent_ran` a `payload.llm_used=false`.

## AI Gemini mode (s Gemini klíčem)
1. Nastav `GEMINI_API_KEY`, `GEMINI_MODEL=gemini-3-flash-preview`, `GEMINI_THINKING_LEVEL=minimal`.
2. Spusť `POST /api/agent/run?incident_id=<uuid>&mode=both`.
3. V `/audit` ověř `action=agent_ran`, `payload.llm_used=true`, `payload.llm_model=gemini-3-flash-preview`.
