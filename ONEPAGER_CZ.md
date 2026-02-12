# OpsBoard (MVP) - Able to compete

## Co to je
OpsBoard je jednoduchý provozní nástroj pro malé týmy. Spojuje:
- board úkolů (Todo / In Progress / Done),
- alerting a eskalaci do incidentů,
- audit log,
- monitoring (`/health`, `/metrics`),
- základní disaster recovery (export/import JSON),
- AI asistenta (Gemini) pro triage i remediation tasky s auditovaným `llm_used` flagem.

## Proč
V challenge čase potřebujeme rychle funkční řešení, které jde snadno vysvětlit i laikovi:
- co se pokazilo (alert),
- co se tím stalo (incident),
- co tým udělal (audit),
- jak to obnovíme (DR),
- co dělat dál (agent návrhy).

## Jak to běží
- Backend/UI: FastAPI + server-rendered HTML (Jinja)
- Data: Supabase Postgres
- Nasazení: Vercel serverless

## Hlavní ukázka (2-3 min)
1. Na boardu vytvořit kartu a přesunout ji do `In Progress`.
2. Vytvořit `critical` alert.
3. Spustit watcher (`run once`) a ukázat vznik incidentu.
4. Otevřít audit log a timeline incidentu.
5. Otevřít monitoring dashboard + `/metrics`.
6. Spustit agenta, který navrhne remediation tasky jako nové karty.

## Co je záměrně MVP tradeoff
- Public demo režim: RLS vypnuté na app tabulkách, explicitní granty.
- Agent bez LLM klíče používá deterministický fallback.
- DR je aplikační export/import, ne plný databázový dump.
