from __future__ import annotations

import argparse
import asyncio
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.settings import settings
from app.db import Base
from app.models import Incident, IncidentEvent, List
from app.services import add_incident_event, create_card
from scripts.llm_client import chat

SYSTEM_PROMPT = (
    "Jsi incident commander a SRE lead. "
    "Piš stručně, konkrétně, bez buzzwordů. Výstup v češtině."
)


def rule_based_summary(inc: Incident, events: list[IncidentEvent]) -> str:
    lines = [
        f"Incident #{inc.id}: {inc.title}",
        f"Severity: {inc.severity.value}, status: {inc.status.value}",
        f"Popis: {inc.description or '(bez popisu)'}",
        "",
        "Poslední události:",
    ]
    for e in events[:5]:
        lines.append(f"- [{e.created_at:%Y-%m-%d %H:%M}] {e.kind}: {e.message}")
    lines.append("")
    lines.append(
        "Další kroky (heuristika):\n"
        "- Ověřit dopad\n"
        "- Stabilizovat\n"
        "- Najít kořenovou příčinu\n"
        "- Přidat guardrails + alerting\n"
    )
    return "\n".join(lines)


async def llm_summary(inc: Incident, events: list[IncidentEvent]) -> str:
    timeline = "\n".join(
        [f"- {e.created_at.isoformat()} [{e.kind}] {e.message}" for e in events[:10]]
    )
    msg = {
        "role": "user",
        "content": (
            "Shrň incident a navrhni 3-5 konkrétních dalších kroků (jako checklist).\n"
            f"Incident:\n- id: {inc.id}\n- title: {inc.title}\n"
            f"- severity: {inc.severity.value}\n- status: {inc.status.value}\n"
            f"- description: {inc.description or ''}\n\n"
            "Timeline (nejnovější nahoře):\n"
            f"{timeline}\n"
        ),
    }
    return await chat([{"role": "system", "content": SYSTEM_PROMPT}, msg], temperature=0.2)


async def llm_tasks(inc: Incident, events: list[IncidentEvent]) -> list[str]:
    ctx_events = "\n".join([f"- {e.kind}: {e.message}" for e in events[:6]])
    msg = {
        "role": "user",
        "content": (
            "Navrhni 4 konkrétní remediation úkoly (krátké názvy) pro incident.\n"
            "Vrať jen odrážky, žádný úvod.\n\n"
            f"Incident: {inc.title}\n"
            f"Severity: {inc.severity.value}\n"
            f"Kontext:\n{inc.description or ''}\n"
            f"Poslední události:\n{ctx_events}\n"
        ),
    }
    txt = await chat([{"role": "system", "content": SYSTEM_PROMPT}, msg], temperature=0.3)
    tasks: list[str] = []
    for line in txt.splitlines():
        line = line.strip()
        if not line:
            continue
        line = line.lstrip("-• ").strip()
        if line:
            tasks.append(line[:120])
    return tasks[:6]


def get_incident(db: Session, incident_id: int) -> tuple[Incident, list[IncidentEvent]]:
    inc = db.get(Incident, incident_id)
    if not inc:
        raise SystemExit("incident not found")
    events = (
        db.execute(
            select(IncidentEvent)
            .where(IncidentEvent.incident_id == incident_id)
            .order_by(IncidentEvent.created_at.desc())
        )
        .scalars()
        .all()
    )
    return inc, events


def get_backlog_list_id(db: Session) -> int:
    lst = db.execute(select(List).where(List.name == "Backlog").limit(1)).scalars().first()
    if not lst:
        raise SystemExit("Backlog list not found")
    return lst.id


async def cmd_summarize(db: Session, incident_id: int):
    inc, events = get_incident(db, incident_id)
    use_llm = bool(os.environ.get("LLM_BASE_URL") and os.environ.get("LLM_API_KEY"))
    out = await llm_summary(inc, events) if use_llm else rule_based_summary(inc, events)
    print(out)
    add_incident_event(
        db,
        inc,
        "update",
        "AI summary generated (see CLI output)",
        actor="agent",
        corr=None,
    )


async def cmd_propose_tasks(db: Session, incident_id: int):
    inc, events = get_incident(db, incident_id)
    use_llm = bool(os.environ.get("LLM_BASE_URL") and os.environ.get("LLM_API_KEY"))
    if use_llm:
        tasks = await llm_tasks(inc, events)
    else:
        tasks = [
            "Změřit dopad a definovat SLO/SLI pro problém",
            "Přidat guardrail (rate limit / circuit breaker) tam, kde to padá",
            "Dopsat testy pro reprodukci incidentu",
            "Zlepšit alerting (redukovat šum, přidat deduplikaci)",
        ]

    backlog_id = get_backlog_list_id(db)
    for t in tasks:
        create_card(
            db,
            backlog_id,
            f"[INC#{inc.id}] {t}",
            None,
            actor="agent",
            corr=None,
        )
    add_incident_event(
        db,
        inc,
        "action",
        f"AI created {len(tasks)} remediation tasks in Backlog",
        actor="agent",
        corr=None,
    )
    print(f"created {len(tasks)} cards in Backlog")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s1 = sp.add_parser("summarize")
    s1.add_argument("--incident-id", type=int, required=True)
    s2 = sp.add_parser("propose-tasks")
    s2.add_argument("--incident-id", type=int, required=True)
    args = ap.parse_args()

    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    engine = create_engine(settings.database_url, connect_args=connect_args)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        if args.cmd == "summarize":
            asyncio.run(cmd_summarize(db, args.incident_id))
        elif args.cmd == "propose-tasks":
            asyncio.run(cmd_propose_tasks(db, args.incident_id))


if __name__ == "__main__":
    main()
