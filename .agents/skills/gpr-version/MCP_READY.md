# MCP / tool-ready rozhraní (rychlý důkaz připravenosti)

MVP má endpoint `GET /api/tools`, který vrací katalog akcí + input schémata.
To je jednoduchý “MCP-style” handshake: agent si umí zjistit, jaké akce systém podporuje,
a pak je volat přes REST.

Pro plnohodnotné MCP by se doplnil:
- transport (stdio/websocket)
- tool invocation wrapper
- auth/permissions

V challenge kontextu tohle stačí jako jasný signál “připraveno na rozšíření”.
