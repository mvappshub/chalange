# OpsBoard MVP (Trello + Betterstack mini-klon)

Tento repozitář je hotové MVP pro challenge **Able to compete**: jednoduchá kanban tabule (Trello-like) + incident management (Betterstack-like), audit log, monitoring, alerting (simulace), DR backup/restore a AI agent pro triage/sumarizaci.

## Rychlý start (lokálně)

### 1) Požadavky
- Python 3.11+
- (volitelně) Docker

### 2) Spuštění bez Dockeru
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Otevři UI: `http://localhost:8000/ui`  
OpenAPI: `http://localhost:8000/docs`

### 3) Spuštění s Docker Compose
```bash
docker compose up --build
```

## Co umí MVP
- **Kanban board**: sloupce + karty; přesun drag&drop.
- **Incidents**: severity, status, timeline událostí.
- **Alerts (simulace)**: vytvoření alertu + **watcher**, který high/critical alert eskaluje na incident.
- **Audit log**: request audit + doménové události (card_created/card_moved/incident_created…).
- **Disaster recovery**: zálohy DB do souboru + restore skript.
- **Monitoring**: `/health` a Prometheus `/metrics`.
- **Dashboard**: jednoduché grafy (Chart.js) pro demo.
- **AI agent (volitelně)**: shrnutí incidentu + návrh remediation úkolů (karty). Umí fallback bez LLM.

## Demo flow (2–3 min)
1) `/ui` → vytvoř kartu a přesuň ji do „In Progress“.  
2) `/ui/alerts` → vytvoř High alert.  
3) Spusť watcher:
```bash
python scripts/watcher.py
```
4) `/ui/incidents` → objeví se auto-incident.  
5) Spusť AI agenta (volitelně):
```bash
python scripts/agent.py summarize --incident-id 1
python scripts/agent.py propose-tasks --incident-id 1
```
6) Ukázat `/ui/audit`, `/metrics`, `/ui/backup`.

## AI agent (volitelné)
Agent používá **OpenAI-compatible** endpoint. Nastav proměnné:
```bash
export LLM_BASE_URL=https://api.openai.com/v1
export LLM_API_KEY="..."
export LLM_MODEL="gpt-4.1-mini"
```
Pozn.: pokud `LLM_*` nenastavíš, agent použije rule-based fallback.

## DR (backup/restore)
```bash
python scripts/backup.py
python scripts/restore.py --file backups/opsboard_YYYYmmdd_HHMMSS.db
```

## Testy + kvalita
```bash
ruff check .
PYTHONPATH=. pytest --cov=app
```

## Struktura
- `app/` FastAPI aplikace (API + UI)
- `app/templates/` HTML šablony
- `app/static/` JS (drag&drop)
- `scripts/` backup/restore, watcher, agent
- `tests/` unit + BDD (pytest-bdd)

## Licence
MIT
