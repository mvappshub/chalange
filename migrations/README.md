# Migrations

Migrations in this folder were applied through Supabase MCP SQL tools (`execute_sql`) and not via Supabase CLI, per challenge constraints.

Applied files:
- `001_init.sql`
- `002_indexes.sql`

Smoke verification after apply (via MCP):
- listed tables in `public`
- inserted and selected rows as `anon` via Supabase REST-compatible grants
