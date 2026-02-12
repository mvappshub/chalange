# Security Review (MVP)

## Input validation
- FastAPI `Form(...)` validační pravidla pro title/severity.
- DB constraints (CHECK) na severity, status, column_name.

## Secrets
- Žádné secrety v repu.
- `.env.example` pouze placeholdery.
- Runtime secrets přes env vars.

## Auth boundaries
- Demo mód: app tabulky v `public` mají RLS OFF + granty pro `anon/authenticated`.
- Není produkční model; pro production zapnout RLS a auth-based policies.

## SQL injection
- Supabase Python client používá strukturované query builder API.
- Přímé SQL používáno jen v migracích přes MCP.

## CORS
- V MVP není široké CORS otevření; app je server-rendered.
- Doporučení: explicitně whitelistnout originy při API-expozici.

## Rate limiting
- Doporučení: edge rate limiting (Vercel/WAF) na `/alerts`, `/watcher/run-once`, `/dr/import`.

## Auditability
- `audit_events` tabulka ukládá doménové změny.
- Request logy mají `request_id`.

## Remaining risks
- Veřejný anon CRUD je zneužitelný (spam/data corruption).
- Chybí autentizace uživatelů.
- Chybí upload anti-malware kontrola pro DR import.
