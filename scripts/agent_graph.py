from __future__ import annotations

import os
from typing import Any

from app.db import build_data_access
from app.services.agent import run_agent_flow


def run_agent(incident_id: str) -> dict[str, Any]:
    db = build_data_access()
    return run_agent_flow(db, incident_id=incident_id, mode="both")


def _langgraph_placeholder() -> str:
    try:
        from langgraph.graph import StateGraph  # type: ignore

        return f"LangGraph available ({StateGraph.__name__}), using functional fallback for deterministic MVP."
    except Exception:
        return "LangGraph not installed, using deterministic fallback graph."


if __name__ == "__main__":
    sample_incident_id = os.getenv("INCIDENT_ID")
    print(_langgraph_placeholder())
    if not sample_incident_id:
        print("Set INCIDENT_ID env var to run the agent.")
    else:
        result = run_agent(sample_incident_id)
        print(result)
