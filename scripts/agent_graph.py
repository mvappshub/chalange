from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any

from app.db import build_data_access


@dataclass
class AgentState:
    incident_id: str
    summary: str = ""
    remediation_tasks: list[str] | None = None


def summarize_fallback(incident: dict[str, Any]) -> str:
    return f"Incident {incident['id']} ({incident['severity']}) is {incident['status']}. Summary: {incident.get('summary', '')}"


def propose_tasks_fallback(incident: dict[str, Any]) -> list[str]:
    return [
        f"Investigate root cause for {incident['title']}",
        "Mitigate customer impact",
        "Publish status page update",
    ]


def summarize_incident(incident: dict[str, Any]) -> str:
    # MVP fallback path when no LLM key is configured.
    if not os.getenv("LLM_API_KEY"):
        return summarize_fallback(incident)
    return summarize_fallback(incident)


def propose_remediation_tasks(incident: dict[str, Any]) -> list[str]:
    if not os.getenv("LLM_API_KEY"):
        return propose_tasks_fallback(incident)
    return propose_tasks_fallback(incident)


def run_agent(incident_id: str) -> dict[str, Any]:
    db = build_data_access()
    incident = db.get_incident(incident_id)
    if not incident:
        raise ValueError("Incident not found")

    summary = summarize_incident(incident)
    tasks = propose_remediation_tasks(incident)
    task_ids = []
    for task in tasks:
        card = db.create_card(title=task, description=f"Auto-generated for incident {incident_id}", column_name="Todo")
        task_ids.append(card["id"])

    db.create_audit_event(
        "agent_actions",
        "incident",
        incident_id,
        {"summary": summary, "task_ids": task_ids, "tasks_count": len(tasks)},
    )
    return {"summary": summary, "task_ids": task_ids}


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
