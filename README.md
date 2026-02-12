# OpsBoard MVP

OpsBoard je challenge MVP pro provozní týmy: board + alerts/incidents + audit + monitoring + DR + AI agent.

## Stack
- Backend/UI: Python, FastAPI, Jinja templates
- DB: Supabase Postgres
- Deploy target: Vercel serverless
- Tests: pytest + pytest-bdd

## Local run
1. Nainstaluj Python 3.11+.
2. Vytvoř `.env` podle `.env.example`.
3. Nainstaluj deps:
   - `pip install -r requirements.txt`
   - `pip install -e .[dev]`
4. Spusť app (Node wrapper):
   - `npm run dev`
5. Otevři `http://localhost:8000`.

## Supabase
DDL/migrace byly aplikovány přes Supabase MCP (viz `migrations/README.md`).

## Tests
- `npm run test`
- `npm run lint`

## BDD
- `tests/features/card_move_audit.feature`
- `tests/features/high_alert_incident.feature`

## Watcher + Agent
- Eskalace alertů: `npm run watcher:once`
- Agent (nastav `INCIDENT_ID`): `npm run agent:demo`

## Monitoring endpoints
- `/health`
- `/metrics`
- `/monitoring`

## DR
- Export: `/dr/export`
- Import: `/dr` (upload JSON)

## Vercel deploy
1. `vercel --prod` (v připojeném projektu/repu)
2. Nastav env vars:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `LLM_API_KEY` (volitelné)
3. Ověř:
   - `/health`
   - `/board`
   - `/tools`

Konfigurace je v `vercel.json`.

## Demo flow
Použij postup z `conductor/spec.md` a storyboard v `video/STORYBOARD.md`.
