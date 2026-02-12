# OpsBoard MVP Spec

## Scope
OpsBoard je jednoduchý "able to compete" MVP nástroj kombinující:
- Trello-like board pro ops úkoly
- Betterstack-like alert -> incident tok
- audit trail a základní monitoring
- jednoduchý DR export/import
- AI agent návrhy remediation tasků

## User Stories
1. Jako on-call engineer chci vytvářet a přesouvat karty mezi `Todo / In Progress / Done`.
2. Jako operátor chci založit alert se severity.
3. Jako incident manager chci high/critical alert eskalovat na incident.
4. Jako auditor chci vidět timeline událostí v audit logu.
5. Jako SRE chci vidět health, metrics a rychlý dashboard.
6. Jako maintainer chci export/import dat (DR drill).
7. Jako ops lead chci AI shrnutí incidentu a návrh remediation tasků.

## Acceptance Criteria
- CRUD karet funguje přes FastAPI + Supabase.
- Přesun karty vytvoří `audit_events.action = card_moved`.
- Alert vytvoření vytvoří `alert_created`.
- Watcher v režimu `--once` vytvoří incident z high/critical alertu.
- Incident detail ukazuje timeline (audit events dle entity_id).
- `/health` vrací `status=ok`, `/metrics` vrací textový export.
- `/tools` vrací JSON kontrakt pro MCP-ready tooling.
- DR export/import funguje JSON souborem.
- BDD testy pokrývají:
  - card move -> audit
  - high alert -> incident

## Demo scénář (2-3 min)
1. Otevřít `/board`, založit kartu, přesunout do `In Progress`, ukázat `/audit`.
2. Otevřít `/alerts`, založit `critical` alert, spustit watcher once.
3. Otevřít `/incidents`, detail incidentu + timeline.
4. Otevřít `/monitoring`, ukázat počty a `/metrics`.
5. Spustit `python scripts/agent_graph.py` s `INCIDENT_ID`, ukázat nové task karty.

## Definition of Done
- Testy `pytest` green.
- Feature files existují a běží.
- App funguje lokálně se Supabase.
- Vercel konfigurace je v repu.
- ONEPAGER_CZ je max 1 strana.
- Demo video je připraveno přes reprodukovatelný render skript.
- Žádné secrety v gitu.
