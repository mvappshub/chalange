# Demo video scénář (2–3 min)

**Cíl:** Ukázat, že to není jen “to-do app”, ale proces: alert → incident → remediation tasks + audit + monitoring + DR.

## 0:00–0:15 Úvod
- Otevři `/ui` a ukaž board.
- Jedna věta: “Kanban + incident response v jednom, audit a metriky built-in.”

## 0:15–0:45 Task workflow
- Vytvoř kartu: “Fix alert storm”.
- Přetáhni ji do “In Progress”.
- Otevři `/ui/audit` a ukaž event `card_moved` (a correlation id v hlavičce).

## 0:45–1:30 Alert → Incident
- Otevři `/ui/alerts`, vytvoř **High** alert “API error rate”.
- V terminálu spusť: `python scripts/watcher.py`
- Otevři `/ui/incidents` → objeví se auto-incident.
- Klikni do incidentu a ukaž timeline (otevření, eskalace).

## 1:30–2:15 AI agent triage
- V terminálu:
  - `python scripts/agent.py summarize --incident-id 1`
  - `python scripts/agent.py propose-tasks --incident-id 1`
- Zpět na `/ui` → v Backlogu se objeví remediation karty s prefixem `[INC#1]`.

## 2:15–2:45 Observability + DR
- Ukaž `/metrics` (Prometheus).
- Ukaž `/ui/dashboard` (grafy).
- Ukaž `/ui/backup` a připomeň: `python scripts/backup.py` (disaster recovery).

## 2:45–3:00 Závěr
- Jedna věta: “MVP je monolit pro rychlost, ale má jasné hranice a tool-catalog `/api/tools` pro MCP/agent rozšíření.”
