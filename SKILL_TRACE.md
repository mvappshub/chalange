# SKILL_TRACE

1. `requirements-clarity` -> definován scope, user stories, acceptance criteria, demo flow, DoD -> `conductor/spec.md`
2. `docs-architect` -> vytvořen onepager + run/deploy/demo dokumentace -> `ONEPAGER_CZ.md`, `README.md`
3. `app-builder` -> vytvořena FastAPI/Jinja architektura + endpoint kostra -> `app/main.py`, `app/templates/*`, `app/static/style.css`, `pyproject.toml`
4. `database-migrations-sql-migrations` -> připraveny SQL migrace + záznam aplikace přes MCP -> `migrations/001_init.sql`, `migrations/002_indexes.sql`, `migrations/README.md`
5. `supabase-development` -> schéma, indexy, granty a smoke anon CRUD -> `migrations/*.sql`, `DECISIONS.md`
6. `observability-guidelines` -> request_id logging middleware, `/health`, `/metrics`, audit-domain events -> `app/obs.py`, `app/main.py`
7. `langgraph` -> agent script summary + remediation tasks + fallback bez LLM -> `scripts/agent_graph.py`
8. `security-review` -> bezpečnostní checklist a rizika -> `SECURITY_REVIEW.md`
9. `code-review-ai-ai-review` -> top 10 rizik, fixy, tradeoffs -> `CODE_REVIEW.md`
10. `mcp-builder` -> tooling readiness + `/tools` kontrakt -> `MCP_READY.md`, `app/main.py`
11. `remotion` -> video skeleton + storyboard + render script -> `video/README.md`, `video/STORYBOARD.md`, `video/render.js`
