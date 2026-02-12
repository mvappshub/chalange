# OpsBoard MVP – 1stránkový popis (pro odeslání)

**Co to je:** OpsBoard je minimalistický systém, který kombinuje kanban řízení úkolů (Trello-like) s provozní spolehlivostí (Betterstack-like): alerty → incidenty → remediation úkoly, plus audit log, monitoring a disaster recovery.

**Pro koho:** Malé i střední týmy, které potřebují univerzální “operational cockpit” bez oborové specializace. UI je záměrně jednoduché a pochopitelné i pro neodborníky.

## Funkce (MVP)
- **Kanban board** se sloupci a kartami + přesun drag&drop.
- **Incident management**: severity, status, timeline událostí (poznámky/akce).
- **Alerting (simulace)**: vytvoření alertu, watcher eskaluje high/critical alert do incidentu.
- **Audit log**: request audit + doménové události (card_created/card_moved/incident_created…).
- **Monitoring**: `/health` a Prometheus `/metrics` (základ pro grafy a alerty).
- **Analytika**: jednoduchý dashboard (počty karet/incidentů/alertů).
- **Disaster recovery**: záloha DB do souboru + restore (jednoduše demonstrovatelné).
- **AI agent (volitelné)**: CLI agent umí incident shrnout a navrhnout remediation úkoly (karty). Funguje i bez LLM klíče (fallback).

## AI-first proces (jak to zrychluje vývoj)
- Zadání → rychlé vytvoření **doménového modelu** (Board/List/Card, Alert, Incident, AuditEvent).
- AI pomocí scénářů (Gherkin) generuje **BDD testy**, které hlídají klíčové procesy (přesun karty → audit; vytvoření alertu).
- AI agent používá “OpenAI-compatible” rozhraní, takže je připravený na výměnu poskytovatele (OpenAI/Anthropic/local gateway).
- Kód je “human made”: čitelný monolit (FastAPI), jasné názvy, minimální magie.

## Release & kvalita
- Dockerfile + docker-compose pro lokální spuštění.
- GitHub Actions CI (lint + test).
- Jednoduchý semver + changelog.

## Demo scénář (2–3 min)
1) Otevřít `/ui`, vytvořit kartu, přetáhnout mezi sloupci.  
2) Otevřít `/ui/alerts`, vytvořit High alert, spustit watcher → incident se otevře.  
3) Spustit agent CLI → vygeneruje shrnutí a vytvoří remediation karty.  
4) Ukázat `/ui/audit`, `/metrics` a `/ui/backup` (backup/restore koncept).

**Repo/URL:** doplníš po uploadu na GitHub a nasazení.
