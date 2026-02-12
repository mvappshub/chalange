# AI Proof Without Vercel Dashboard

Tento postup prokazuje "AI powered" i bez pristupu do Vercel dashboardu.

## 1) Spusteni API callu

Pouzij presne:

```bash
curl -X POST "https://chalange-three.vercel.app/api/agent/run?incident_id=<INCIDENT_ID>&mode=both"
```

Poznamka:
- `<INCIDENT_ID>` vezmi z URL detailu incidentu (`/incidents/<INCIDENT_ID>`), nebo z listu incidentu.

## 2) Co musi byt v odpovedi

V JSON odpovedi musi byt videt:
- `llm_used=true`
- `llm_model=gemini-3-flash-preview`
- `thinking_level=minimal`
- `task_ids` (neprazdne pole)

## 3) Dukazni screenshoty

Udelej 2 screenshoty:

1. Terminal:
- screenshot terminalu s `curl` prikazem a celou JSON odpovedi
- musi byt videt `llm_used=true`

2. Audit:
- otevri `https://chalange-three.vercel.app/audit`
- najdi `agent_ran`
- otevri `View JSON`
- screenshot, kde je videt `llm_used=true` (a idealne i `llm_model`)

## 4) Co prilozit do submission

- 2 screenshoty vyse
- odkaz na produkcni URL
- odkaz na repo
- onepager + demo video
