# MCP Ready Notes

OpsBoard exposes tool contract endpoint:
- `GET /tools`

Purpose:
- Describe internal tool-like operations for future MCP server wrapping.

Current contract:
- `summarize_incident(incident_id)` -> summary text
- `create_remediation_tasks(incident_id)` -> created card IDs

Recommended MCP extension path:
1. Wrap these operations in dedicated MCP server (Python FastMCP or Node MCP SDK).
2. Add auth and schema validation (JSON Schema).
3. Expose DB-safe operations only (no raw SQL).
