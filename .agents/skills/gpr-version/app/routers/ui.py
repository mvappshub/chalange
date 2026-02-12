from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models, services

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/ui", tags=["ui"])


def _board_view(db: Session):
    services.ensure_seed(db)
    board = db.query(models.Board).filter(models.Board.name == "OpsBoard").first()
    lists = (
        db.query(models.List)
        .filter(models.List.board_id == board.id)
        .order_by(models.List.position)
        .all()
    )
    data = []
    for lst in lists:
        cards = (
            db.query(models.Card)
            .filter(models.Card.list_id == lst.id)
            .order_by(models.Card.created_at.desc())
            .all()
        )
        data.append((lst, cards))
    return board, data


@router.get("", response_class=HTMLResponse)
def ui_home(request: Request, db: Session = Depends(get_db)):
    board, lists = _board_view(db)
    return templates.TemplateResponse("board.html", {"request": request, "board": board, "lists": lists})


@router.post("/cards/create")
def ui_create_card(
    request: Request,
    title: str = Form(...),
    description: str | None = Form(None),
    list_id: int = Form(...),
    db: Session = Depends(get_db),
):
    corr = getattr(request.state, "correlation_id", None)
    services.create_card(db, list_id, title, description, actor="anonymous", corr=corr)
    return RedirectResponse(url="/ui", status_code=303)


@router.post("/cards/{card_id}/move")
def ui_move_card(request: Request, card_id: int, list_id: int = Form(...), db: Session = Depends(get_db)):
    corr = getattr(request.state, "correlation_id", None)
    card = db.get(models.Card, card_id)
    if card:
        services.move_card(db, card, list_id, actor="anonymous", corr=corr)
    return HTMLResponse("OK")


@router.get("/incidents", response_class=HTMLResponse)
def ui_incidents(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Incident).order_by(models.Incident.created_at.desc()).all()
    return templates.TemplateResponse("incidents.html", {"request": request, "incidents": items})


@router.post("/incidents/create")
def ui_create_incident(
    request: Request,
    title: str = Form(...),
    description: str | None = Form(None),
    severity: str = Form("medium"),
    db: Session = Depends(get_db),
):
    corr = getattr(request.state, "correlation_id", None)
    sev = models.Severity(severity)
    services.create_incident(db, title, description, sev, actor="anonymous", corr=corr)
    return RedirectResponse(url="/ui/incidents", status_code=303)


@router.get("/incidents/{incident_id}", response_class=HTMLResponse)
def ui_incident_detail(request: Request, incident_id: int, db: Session = Depends(get_db)):
    inc = db.get(models.Incident, incident_id)
    events = (
        db.query(models.IncidentEvent)
        .filter(models.IncidentEvent.incident_id == incident_id)
        .order_by(models.IncidentEvent.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        "incident_detail.html",
        {"request": request, "incident": inc, "events": events},
    )


@router.post("/incidents/{incident_id}/events")
def ui_add_incident_event(
    request: Request,
    incident_id: int,
    kind: str = Form("note"),
    message: str = Form(...),
    db: Session = Depends(get_db),
):
    corr = getattr(request.state, "correlation_id", None)
    inc = db.get(models.Incident, incident_id)
    if inc:
        services.add_incident_event(db, inc, kind, message, actor="anonymous", corr=corr)
    return RedirectResponse(url=f"/ui/incidents/{incident_id}", status_code=303)


@router.get("/alerts", response_class=HTMLResponse)
def ui_alerts(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Alert).order_by(models.Alert.created_at.desc()).all()
    return templates.TemplateResponse("alerts.html", {"request": request, "alerts": items})


@router.post("/alerts/create")
def ui_create_alert(
    request: Request,
    name: str = Form(...),
    severity: str = Form("medium"),
    source: str = Form("manual"),
    message: str | None = Form(None),
    db: Session = Depends(get_db),
):
    corr = getattr(request.state, "correlation_id", None)
    sev = models.Severity(severity)
    services.create_alert(db, name, sev, source, message, actor="anonymous", corr=corr)
    return RedirectResponse(url="/ui/alerts", status_code=303)


@router.get("/audit", response_class=HTMLResponse)
def ui_audit(request: Request, db: Session = Depends(get_db)):
    rows = db.query(models.AuditEvent).order_by(models.AuditEvent.at.desc()).limit(200).all()
    return templates.TemplateResponse("audit.html", {"request": request, "rows": rows})


@router.get("/dashboard", response_class=HTMLResponse)
def ui_dashboard(request: Request, db: Session = Depends(get_db)):
    # minimal analytics: counts by list, incidents by status, alerts by severity
    board, lists = _board_view(db)
    list_counts = [{"name": lst.name, "count": len(cards)} for lst, cards in lists]

    by_status: dict[str, int] = {}
    for st, _ in db.query(models.Incident.status, models.Incident.id).all():
        by_status[st.value] = by_status.get(st.value, 0) + 1

    by_sev: dict[str, int] = {}
    for sev, _ in db.query(models.Alert.severity, models.Alert.id).all():
        by_sev[sev.value] = by_sev.get(sev.value, 0) + 1

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "board": board,
            "list_counts": list_counts,
            "inc_by_status": by_status,
            "alerts_by_severity": by_sev,
        },
    )


@router.get("/backup", response_class=HTMLResponse)
def ui_backup(request: Request):
    # list existing backups
    import os

    os.makedirs("backups", exist_ok=True)
    files = sorted(os.listdir("backups"), reverse=True)
    return templates.TemplateResponse("backup.html", {"request": request, "files": files})
