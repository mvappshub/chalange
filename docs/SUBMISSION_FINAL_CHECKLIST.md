# Submission Final Checklist

## 1) Deliverables (must have)

- [ ] Repo link: `https://github.com/mvappshub/chalange`
- [ ] Vercel URL: `https://chalange-three.vercel.app`
- [ ] Onepager: `ONEPAGER_CZ.md`
- [ ] Demo video: `video/out/demo.mp4` (nebo export podle `video/README.md`)
- [ ] Submission email: `SUBMISSION_EMAIL_CZ.txt`

## 2) AI proof (no-dashboard path)

- [ ] Spustit:

```bash
curl -X POST "https://chalange-three.vercel.app/api/agent/run?incident_id=<INCIDENT_ID>&mode=both"
```

- [ ] Ověřit v odpovědi:
  - `llm_used=true`
  - `llm_model=gemini-3-flash-preview`
  - `thinking_level=minimal`
  - `task_ids`
- [ ] Screenshot terminálu s příkazem + odpovědí.
- [ ] Screenshot `https://chalange-three.vercel.app/audit` -> `agent_ran` -> `View JSON` s `llm_used=true`.

## 3) Co natočit do videa (krátce, jasně)

- [ ] Otevřít `/alerts`, vytvořit HIGH alert a spustit eskalaci.
- [ ] Otevřít vytvořený incident.
- [ ] Spustit AI akce (`Run AI triage`, `Propose tasks`).
- [ ] Otevřít `/board` a ukázat vytvořené remediation karty.
- [ ] Otevřít `/audit` a ukázat `agent_ran`.
- [ ] Otevřít `/monitoring` a `/metrics`.

## 4) Login issue fallback

- [ ] Pokud Vercel dashboard nefunguje, pokračovat bez něj:
  - důkaz běhu přes veřejné URL
  - AI proof přes curl + audit screenshot
  - všechny odkazy dodat v emailu
- [ ] Login fix loop je v `docs/VERCEL_LOGIN_TROUBLESHOOT.md`.
