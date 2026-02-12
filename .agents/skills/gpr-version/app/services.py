from __future__ import annotations

import hashlib
from datetime import datetime

from sqlalchemy.orm import Session

from . import models
from .audit import log_event


def ensure_seed(db: Session) -> None:
    board = db.query(models.Board).filter(models.Board.name == "OpsBoard").first()
    if board:
        return
    board = models.Board(name="OpsBoard")
    db.add(board)
    db.commit()
    db.refresh(board)

    lists = [
        models.List(board_id=board.id, name="Backlog", position=1),
        models.List(board_id=board.id, name="In Progress", position=2),
        models.List(board_id=board.id, name="Done", position=3),
    ]
    db.add_all(lists)
    db.commit()

    log_event(db, actor="system", action="board_seeded", entity_type="board", entity_id=board.id)


def create_card(
    db: Session,
    list_id: int,
    title: str,
    description: str | None,
    actor: str,
    corr: str | None,
):
    card = models.Card(list_id=list_id, title=title, description=description)
    db.add(card)
    db.commit()
    db.refresh(card)
    log_event(
        db,
        actor=actor,
        action="card_created",
        entity_type="card",
        entity_id=card.id,
        correlation_id=corr,
        details={"list_id": list_id, "title": title},
    )
    return card


def move_card(db: Session, card: models.Card, new_list_id: int, actor: str, corr: str | None):
    old_list_id = card.list_id
    card.list_id = new_list_id
    card.updated_at = datetime.utcnow()
    db.add(card)
    db.commit()
    log_event(
        db,
        actor=actor,
        action="card_moved",
        entity_type="card",
        entity_id=card.id,
        correlation_id=corr,
        details={"from_list_id": old_list_id, "to_list_id": new_list_id},
    )


def create_incident(
    db: Session,
    title: str,
    description: str | None,
    severity: models.Severity,
    actor: str,
    corr: str | None,
):
    inc = models.Incident(title=title, description=description, severity=severity)
    db.add(inc)
    db.commit()
    db.refresh(inc)
    log_event(
        db,
        actor=actor,
        action="incident_created",
        entity_type="incident",
        entity_id=inc.id,
        correlation_id=corr,
        details={"severity": severity.value, "title": title},
    )
    db.add(models.IncidentEvent(incident_id=inc.id, kind="note", message="Incident opened"))
    db.commit()
    return inc


def add_incident_event(
    db: Session,
    inc: models.Incident,
    kind: str,
    message: str,
    actor: str,
    corr: str | None,
):
    ev = models.IncidentEvent(incident_id=inc.id, kind=kind, message=message)
    db.add(ev)
    db.commit()
    log_event(
        db,
        actor=actor,
        action="incident_event_added",
        entity_type="incident",
        entity_id=inc.id,
        correlation_id=corr,
        details={"kind": kind, "message": message[:200]},
    )


def fingerprint_alert(name: str, source: str, message: str | None) -> str:
    s = f"{name}|{source}|{message or ''}".encode("utf-8")
    return hashlib.sha256(s).hexdigest()[:32]


def create_alert(
    db: Session,
    name: str,
    severity: models.Severity,
    source: str,
    message: str | None,
    actor: str,
    corr: str | None,
):
    fp = fingerprint_alert(name, source, message)
    alert = models.Alert(name=name, severity=severity, source=source, message=message, fingerprint=fp)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    log_event(
        db,
        actor=actor,
        action="alert_created",
        entity_type="alert",
        entity_id=alert.id,
        correlation_id=corr,
        details={"severity": severity.value, "fingerprint": fp, "source": source},
    )
    return alert
