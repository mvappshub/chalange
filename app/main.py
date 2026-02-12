from __future__ import annotations

from datetime import datetime, timezone
import io
import json
from typing import Any

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.db import DataAccess, build_data_access
from app.obs import RequestContextMiddleware, configure_logging, log_event, metrics
from app.services.agent import run_agent_flow


configure_logging()
app = FastAPI(title="OpsBoard")
app.add_middleware(RequestContextMiddleware)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def get_data_access() -> DataAccess:
    return build_data_access()


def split_cards(cards: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    columns = {"Todo": [], "In Progress": [], "Done": []}
    for card in cards:
        columns.setdefault(card["column_name"], []).append(card)
    return columns


@app.get("/", response_class=HTMLResponse)
def root() -> RedirectResponse:
    return RedirectResponse("/board", status_code=302)


@app.get("/board", response_class=HTMLResponse)
def board_page(request: Request, db: DataAccess = Depends(get_data_access)):
    cards = db.list_cards()
    return templates.TemplateResponse(
        request,
        "board.html",
        {
            "app_name": get_settings().app_name,
            "request": request,
            "columns": split_cards(cards),
        },
    )


@app.post("/cards")
def create_card(
    request: Request,
    title: str = Form(..., min_length=2, max_length=120),
    description: str = Form("", max_length=500),
    column_name: str = Form("Todo"),
    db: DataAccess = Depends(get_data_access),
):
    db.create_card(title=title, description=description, column_name=column_name)
    log_event("domain_event", request_id=request.state.request_id, action="card_created")
    return RedirectResponse("/board", status_code=303)


@app.post("/cards/{card_id}/move")
def move_card(
    card_id: str,
    request: Request,
    column_name: str = Form(...),
    db: DataAccess = Depends(get_data_access),
):
    db.move_card(card_id, column_name)
    log_event("domain_event", request_id=request.state.request_id, action="card_moved", card_id=card_id)
    return RedirectResponse("/board", status_code=303)


@app.post("/cards/{card_id}/delete")
def delete_card(card_id: str, db: DataAccess = Depends(get_data_access)):
    db.delete_card(card_id)
    return RedirectResponse("/board", status_code=303)


@app.get("/alerts", response_class=HTMLResponse)
def alerts_page(request: Request, db: DataAccess = Depends(get_data_access)):
    return templates.TemplateResponse(
        request, "alerts.html", {"request": request, "alerts": db.list_alerts(), "app_name": get_settings().app_name}
    )


@app.post("/alerts")
def create_alert(
    request: Request,
    title: str = Form(..., min_length=3, max_length=120),
    severity: str = Form(..., pattern="^(low|medium|high|critical)$"),
    source: str = Form("manual"),
    db: DataAccess = Depends(get_data_access),
):
    alert = db.create_alert(title=title, severity=severity, source=source)
    log_event("domain_event", request_id=request.state.request_id, action="alert_created", alert_id=alert["id"])
    return RedirectResponse("/alerts", status_code=303)


@app.post("/watcher/run-once")
def run_watcher_once(request: Request, db: DataAccess = Depends(get_data_access)):
    created = 0
    for alert in db.list_unescalated_high_alerts():
        db.create_incident_from_alert(alert)
        created += 1
    db.create_audit_event("watcher_run", "system", "watcher", {"created_incidents": created})
    log_event("domain_event", request_id=request.state.request_id, action="watcher_run", created=created)
    return RedirectResponse("/incidents", status_code=303)


@app.get("/incidents", response_class=HTMLResponse)
def incidents_page(request: Request, db: DataAccess = Depends(get_data_access)):
    return templates.TemplateResponse(
        request,
        "incidents.html",
        {"request": request, "incidents": db.list_incidents(), "app_name": get_settings().app_name},
    )


@app.get("/incidents/{incident_id}", response_class=HTMLResponse)
def incident_detail(request: Request, incident_id: str, db: DataAccess = Depends(get_data_access)):
    incident = db.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    timeline = db.list_audit_for_entity(incident_id)
    notes = db.list_incident_notes(incident_id)
    triage_note = next((n for n in notes if n["note_type"] == "triage"), None)
    remediation_cards = db.list_agent_cards_for_incident(incident_id)
    return templates.TemplateResponse(
        request,
        "incident_detail.html",
        {
            "request": request,
            "incident": incident,
            "timeline": timeline,
            "triage_note": triage_note,
            "remediation_cards": remediation_cards,
            "app_name": get_settings().app_name,
        },
    )


@app.post("/incidents/{incident_id}/status")
def incident_update_status(incident_id: str, status: str = Form(...), db: DataAccess = Depends(get_data_access)):
    db.update_incident_status(incident_id, status)
    return RedirectResponse(f"/incidents/{incident_id}", status_code=303)


@app.get("/audit", response_class=HTMLResponse)
def audit_page(request: Request, db: DataAccess = Depends(get_data_access)):
    events = db.list_audit_events()
    return templates.TemplateResponse(
        request, "audit.html", {"request": request, "events": events, "app_name": get_settings().app_name}
    )


@app.get("/monitoring", response_class=HTMLResponse)
def monitoring_page(request: Request, db: DataAccess = Depends(get_data_access)):
    counts = db.counts()
    return templates.TemplateResponse(
        request,
        "monitoring.html",
        {"request": request, "counts": counts, "metrics": metrics, "app_name": get_settings().app_name},
    )


@app.get("/health")
def health(db: DataAccess = Depends(get_data_access)):
    db.counts()
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.get("/metrics")
def metrics_endpoint(db: DataAccess = Depends(get_data_access)):
    counts = db.counts()
    body = "\n".join(
        [
            "# HELP opsboard_requests_total Total HTTP requests",
            "# TYPE opsboard_requests_total counter",
            f"opsboard_requests_total {metrics.requests_total}",
            "# HELP opsboard_request_latency_ms_avg Average request latency",
            "# TYPE opsboard_request_latency_ms_avg gauge",
            f"opsboard_request_latency_ms_avg {metrics.request_latency_ms_avg:.2f}",
            "# HELP opsboard_entities_total Total entities by table",
            "# TYPE opsboard_entities_total gauge",
            f"opsboard_entities_total{{table=\"cards\"}} {counts['cards']}",
            f"opsboard_entities_total{{table=\"alerts\"}} {counts['alerts']}",
            f"opsboard_entities_total{{table=\"incidents\"}} {counts['incidents']}",
            f"opsboard_entities_total{{table=\"audit_events\"}} {counts['audit_events']}",
            f"opsboard_entities_total{{table=\"incident_notes\"}} {counts['incident_notes']}",
        ]
    )
    return PlainTextResponse(body + "\n")


@app.post("/api/agent/run")
def agent_run_api(
    request: Request,
    incident_id: str,
    mode: str = "both",
    db: DataAccess = Depends(get_data_access),
):
    if mode not in {"triage", "plan", "both"}:
        raise HTTPException(status_code=400, detail="mode must be triage, plan, or both")
    try:
        result = run_agent_flow(db, incident_id=incident_id, mode=mode)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    log_event(
        "domain_event",
        request_id=request.state.request_id,
        action="agent_ran",
        incident_id=incident_id,
        mode=mode,
        llm_used=result["llm_used"],
        llm_model=result["llm_model"],
    )
    return JSONResponse(result)


@app.get("/dr", response_class=HTMLResponse)
def dr_page(request: Request):
    return templates.TemplateResponse(request, "dr.html", {"request": request, "app_name": get_settings().app_name})


@app.get("/dr/export")
def dr_export(db: DataAccess = Depends(get_data_access)):
    payload = db.export_all()
    blob = io.BytesIO(json.dumps(payload, ensure_ascii=True, indent=2).encode("utf-8"))
    return StreamingResponse(
        blob,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=opsboard-backup.json"},
    )


@app.post("/dr/import")
async def dr_import(file: UploadFile = File(...), db: DataAccess = Depends(get_data_access)):
    raw = await file.read()
    payload = json.loads(raw.decode("utf-8"))
    db.import_all(payload)
    db.create_audit_event("dr_import", "system", "backup", {"tables": list(payload.keys())})
    return RedirectResponse("/monitoring", status_code=303)


@app.get("/tools")
def tools_descriptor():
    return JSONResponse(
        {
            "name": "opsboard-tools",
            "version": "0.1.0",
            "tools": [
                {
                    "name": "summarize_incident",
                    "input": {"incident_id": "uuid"},
                    "output": {"summary": "string"},
                },
                {
                    "name": "create_remediation_tasks",
                    "input": {"incident_id": "uuid"},
                    "output": {"task_ids": ["uuid"]},
                },
            ],
        }
    )
