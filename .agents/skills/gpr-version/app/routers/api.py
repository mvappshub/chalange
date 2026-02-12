from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models, schemas, services

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/boards/default")
def get_default_board(db: Session = Depends(get_db)):
    services.ensure_seed(db)
    board = db.query(models.Board).filter(models.Board.name == "OpsBoard").first()
    lists = (
        db.query(models.List)
        .filter(models.List.board_id == board.id)
        .order_by(models.List.position)
        .all()
    )
    out = {"id": board.id, "name": board.name, "lists": []}
    for lst in lists:
        cards = (
            db.query(models.Card)
            .filter(models.Card.list_id == lst.id)
            .order_by(models.Card.created_at.desc())
            .all()
        )
        out["lists"].append(
            {
                "id": lst.id,
                "name": lst.name,
                "position": lst.position,
                "cards": [{"id": c.id, "title": c.title, "description": c.description} for c in cards],
            }
        )
    return out


@router.post("/cards")
def create_card(payload: schemas.CardCreate, db: Session = Depends(get_db)):
    card = services.create_card(
        db,
        payload.list_id,
        payload.title,
        payload.description,
        actor="anonymous",
        corr=None,
    )
    return {"id": card.id}


@router.post("/cards/{card_id}/move")
def move_card(card_id: int, payload: schemas.CardMove, db: Session = Depends(get_db)):
    card = db.get(models.Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="card not found")
    services.move_card(db, card, payload.list_id, actor="anonymous", corr=None)
    return {"ok": True}


@router.post("/incidents")
def create_incident(payload: schemas.IncidentCreate, db: Session = Depends(get_db)):
    inc = services.create_incident(
        db,
        payload.title,
        payload.description,
        payload.severity,
        actor="anonymous",
        corr=None,
    )
    return {"id": inc.id}


@router.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    items = db.query(models.Incident).order_by(models.Incident.created_at.desc()).all()
    return [
        {"id": i.id, "title": i.title, "severity": i.severity.value, "status": i.status.value}
        for i in items
    ]


@router.post("/incidents/{incident_id}/events")
def add_incident_event(
    incident_id: int,
    payload: schemas.IncidentEventCreate,
    db: Session = Depends(get_db),
):
    inc = db.get(models.Incident, incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="incident not found")
    services.add_incident_event(db, inc, payload.kind, payload.message, actor="anonymous", corr=None)
    return {"ok": True}


@router.post("/alerts")
def create_alert(payload: schemas.AlertCreate, db: Session = Depends(get_db)):
    alert = services.create_alert(
        db,
        payload.name,
        payload.severity,
        payload.source,
        payload.message,
        actor="anonymous",
        corr=None,
    )
    return {"id": alert.id, "fingerprint": alert.fingerprint}


@router.get("/audit")
def list_audit(limit: int = 50, db: Session = Depends(get_db)):
    rows = db.query(models.AuditEvent).order_by(models.AuditEvent.at.desc()).limit(limit).all()
    return [schemas.AuditOut.model_validate(r).model_dump() for r in rows]

@router.get("/tools")
def tools():
    """Lightweight MCP-style tool catalog (JSON schema-ish)."""
    return {
        "tools": [
            {
                "name": "create_card",
                "description": "Create a kanban card",
                "input_schema": {
                    "type": "object",
                    "required": ["title", "list_id"],
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": ["string", "null"]},
                        "list_id": {"type": "integer"},
                    },
                },
                "endpoint": {"method": "POST", "path": "/api/cards"},
            },
            {
                "name": "move_card",
                "description": "Move a card to another list",
                "input_schema": {
                    "type": "object",
                    "required": ["list_id"],
                    "properties": {"list_id": {"type": "integer"}},
                },
                "endpoint": {"method": "POST", "path": "/api/cards/{card_id}/move"},
            },
            {
                "name": "create_incident",
                "description": "Open an incident",
                "input_schema": {
                    "type": "object",
                    "required": ["title"],
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": ["string", "null"]},
                        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                    },
                },
                "endpoint": {"method": "POST", "path": "/api/incidents"},
            },
            {
                "name": "add_incident_event",
                "description": "Append a timeline event",
                "input_schema": {
                    "type": "object",
                    "required": ["message"],
                    "properties": {
                        "kind": {"type": "string"},
                        "message": {"type": "string"},
                    },
                },
                "endpoint": {"method": "POST", "path": "/api/incidents/{incident_id}/events"},
            },
            {
                "name": "create_alert",
                "description": "Create an alert (simulated monitoring signal)",
                "input_schema": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                        "source": {"type": "string"},
                        "message": {"type": ["string", "null"]},
                    },
                },
                "endpoint": {"method": "POST", "path": "/api/alerts"},
            },
        ]
    }
