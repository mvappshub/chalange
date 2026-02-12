from __future__ import annotations

import os
from typing import Any

from app.obs import log_event
from app.services.llm_gemini import LLMUnavailable, generate_text


def summarize_fallback(incident: dict[str, Any]) -> str:
    return (
        f"Incident {incident['id']} ({incident['severity']}) is {incident['status']}. "
        f"Current summary: {incident.get('summary', '')}"
    )


def propose_tasks_fallback(incident: dict[str, Any]) -> list[str]:
    return [
        f"Investigate root cause for {incident['title']}",
        "Mitigate customer impact",
        "Write incident update for stakeholders",
    ]


def _meta(llm_used: bool) -> dict[str, Any]:
    return {
        "llm_used": llm_used,
        "llm_model": os.getenv("GEMINI_MODEL", "gemini-3-flash-preview"),
        "thinking_level": os.getenv("GEMINI_THINKING_LEVEL", "minimal"),
    }


def _llm_or_fallback(prompt: str, fallback_value: Any) -> tuple[Any, dict[str, Any]]:
    try:
        text = generate_text(prompt, thinking_level=os.getenv("GEMINI_THINKING_LEVEL", "minimal"))
        return text, _meta(True)
    except LLMUnavailable:
        return fallback_value, _meta(False)


def _parse_tasks(text: str) -> list[str]:
    tasks = [line.strip("- ").strip() for line in text.splitlines() if line.strip()]
    return [t for t in tasks if t][:5]


def run_agent_flow(db, incident_id: str, mode: str) -> dict[str, Any]:
    incident = db.get_incident(incident_id)
    if not incident:
        raise ValueError("Incident not found")

    summary = ""
    task_ids: list[str] = []
    llm_used = False
    llm_model = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
    thinking_level = os.getenv("GEMINI_THINKING_LEVEL", "minimal")

    if mode in ["triage", "both"]:
        prompt = (
            "You are incident response assistant. Write concise Czech triage summary with impact, likely cause, "
            "and immediate next steps.\n\n"
            f"Incident title: {incident['title']}\n"
            f"Severity: {incident['severity']}\n"
            f"Status: {incident['status']}\n"
            f"Summary: {incident.get('summary', '')}\n"
        )
        triage_fallback = summarize_fallback(incident)
        summary_or_fallback, meta = _llm_or_fallback(prompt, triage_fallback)
        summary = summary_or_fallback
        llm_used = llm_used or meta["llm_used"]
        db.upsert_incident_note(incident_id, "triage", summary)

    if mode in ["plan", "both"]:
        prompt = (
            "Navrhni 3-5 remediation tasku pro incident. Vrat jen odrazky, kazda odrazka jedna task veta.\n\n"
            f"Incident title: {incident['title']}\n"
            f"Severity: {incident['severity']}\n"
            f"Status: {incident['status']}\n"
            f"Summary: {incident.get('summary', '')}\n"
        )
        tasks_fallback = propose_tasks_fallback(incident)
        tasks_text_or_fallback, meta = _llm_or_fallback(prompt, "\n".join(tasks_fallback))
        llm_used = llm_used or meta["llm_used"]
        tasks = _parse_tasks(tasks_text_or_fallback) if meta["llm_used"] else tasks_fallback
        for task in tasks:
            card = db.create_card(
                title=task,
                description=f"Auto-generated remediation for incident {incident_id}",
                column_name="Todo",
            )
            task_ids.append(card["id"])

    payload = {
        "mode": mode,
        "llm_used": llm_used,
        "llm_model": llm_model,
        "thinking_level": thinking_level,
        "task_ids": task_ids,
        "tasks_count": len(task_ids),
        "summary_preview": summary[:220] if summary else "",
    }
    db.create_audit_event("agent_ran", "incident", incident_id, payload)
    log_event(
        "agent_run",
        incident_id=incident_id,
        mode=mode,
        llm_used=llm_used,
        llm_model=llm_model,
        thinking_level=thinking_level,
        tasks_count=len(task_ids),
    )
    return {
        "summary": summary,
        "task_ids": task_ids,
        "llm_used": llm_used,
        "llm_model": llm_model,
        "thinking_level": thinking_level,
    }
