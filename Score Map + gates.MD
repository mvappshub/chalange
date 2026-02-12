Jdu na to: převedu “Score Map + gates” do **agentní task tabule**, kterou můžeš rovnou nalít do AI-IDE (Cursor / Windsurf) a jet. A beru jako závazné tvoje strategické rozhodnutí: **Návrh #2 = Python/FastAPI + SSR šablony + HTMX + skripty pro Ops** (BDD, metrics, DR, watcher, agent).

Níže je to napsané tak, aby to maximalizovalo šanci na výhru: každá práce musí vyprodukovat **důkaz** (artefakt) viditelný v demu / repo / URL.

---

## A) Nastavení “agentního režimu” (jednorázové)

Tohle není feature práce – to je režie, která ti zrychlí všechno.

### A1) Role agentů (pevně dané)

* **ORCH (Orchestrator / Lead):** prioritizace po 30–45 min blocích, scope kontrola, “ship / drop” rozhodnutí.
* **SPEC (Architect + Spec writer):** kontrakty + doménové události + rozhodnutí.
* **QA (BDD/Testing):** `.feature`, pytest-bdd, smoke.
* **SRE (Ops):** metrics/health/logging, incident workflow, DR skripty.
* **UI (SSR/HTMX):** board UI + incident/alerts/audit stránky.
* **AI (Agents):** `agent.py` + tool katalog (`/tools`) + audit stopa AI akcí.
* **REVIEW (Red Team / Code review):** rozbije tvé ego dřív, než to udělá porota.

### A2) Jedno pravidlo, které vyhrává challenge

**Každý ticket musí mít “Evidence line”:** *Jak to hodnotitel uvidí za 5 sekund?*
Pokud to neumíš říct jednou větou, ticket je podezřelý a jde pryč.

---

## B) “Score Map” ve formě důkazů (co musí být vidět)

Tohle je tvůj kompas pro rozhodování, ne seznam funkcí.

* **AI agenti:** video z terminálu + audit stopa + změny v DB/UI po běhu agenta
* **BDD:** `.feature` soubor + běh `pytest` zeleně (ukázat v demu)
* **Monitoring:** `/metrics` (Prometheus text) + `/health`
* **Incident response:** “alert → watcher → incident timeline” viditelně
* **Audit log:** stránka / endpoint, kde je `card_moved`, `alert_escalated`, `agent_ran`
* **DR:** `backup.py` a `restore.py` + mini ukázka v demu
* **Release:** tag/verze + krátký changelog + “jak spustit”
* **Human-made:** konzistentní struktura, rozhodnutí v docs, čitelné názvy, žádná magie

---

## C) Gate systém (tvé 4 rozhodovací brány)

**Gate 1 – E2E slice žije:** UI → API → DB → audit → UI refresh
**Gate 2 – Ops důkaz:** `/health` + `/metrics` + základ logů s request id
**Gate 3 – Incident flow:** alert → (watcher) → incident + timeline + audit
**Gate 4 – Agent proof:** agent triage + návrh tasků + audit + nové karty

Když se někde zasekneš: **dropni vše, co není gate**, ne gate.

---

## D) Agentní task tabule (copy-paste prompty + vstupy/výstupy + důkaz)

Každý ticket má: **Owner agent → Timebox → Inputs → Outputs → Evidence → Prompt pro agenta**

### T00 — ORCH: Založení “Mission Control”

* **Owner:** ORCH
* **Timebox:** 10 min
* **Inputs:** zadání, Score Map, Gates
* **Outputs:** `/docs/DoD.md` (checklist), `/docs/PLAN.md` (časové bloky), `/docs/RISKS.md` (Top 5 rizik + mitigace)
* **Evidence:** porota vidí disciplínu procesu už v repo
* **Prompt:**

  > Vytvoř DoD checklist podle bodů challenge + 4 gates. Napiš krátký časový plán po 30min blocích a risk register (5 rizik, mitigace). Udrž to na 1–2 obrazovky na soubor.

---

### T01 — SPEC: Kontrakt domény + události (contract-first)

* **Owner:** SPEC
* **Timebox:** 25 min
* **Inputs:** Score Map + thin slice “alert→incident→agent→tasks”
* **Outputs:** `/docs/SPEC.md` (entity + eventy), `/docs/API.md` (endpointy + payloady)
* **Evidence:** ukážeš “doménové události” + audit vocabulary
* **Prompt:**

  > Navrhni minimální doménový model (board/list/card, alert, incident, incident_event, audit_event, backup). Definuj doménové eventy jako slovník (např. card_moved…). Navrhni minimal API endpoints (CRUD jen tam, kde to potřebuje demo). Vše tak, aby šlo přímo implementovat ve FastAPI.

---

### T02 — QA: BDD scénáře jako definice pravdy

* **Owner:** QA
* **Timebox:** 25 min
* **Inputs:** `/docs/SPEC.md`, `/docs/API.md`
* **Outputs:** `features/*.feature` (3–5 scénářů) + `/docs/TESTPLAN.md`
* **Evidence:** porota uvidí `.feature` a zelené testy
* **Prompt:**

  > Napiš 4 Gherkin scénáře: (1) přesun karty vytvoří audit, (2) vytvoření high alertu + watcher eskaluje incident, (3) backup+restore vrátí data, (4) agent vytvoří remediation karty a zapíše audit. Připrav i stručný TESTPLAN: jak to spustit a jaké jsou očekávané výsledky.

---

### T03 — Repo skeleton + quality gates

* **Owner:** UI (nebo “Repo Engineer” pokud ho máš)
* **Timebox:** 20 min
* **Inputs:** SPEC + BDD
* **Outputs:** struktura projektu + `requirements.txt` + `pyproject`/`ruff` + CI workflow + basic FastAPI app běží
* **Evidence:** “jedním příkazem to běží”, CI pipeline existuje
* **Prompt:**

  > Vytvoř skeleton FastAPI projektu s templaty (Jinja2), static, scripts, tests, features. Přidej ruff/pytest-bdd, a GitHub Actions workflow (lint+tests). Připrav README: run lokálně.

*(Pokud už máš existující skeleton, tohle je jen “normalizace” a doplnění guardrails.)*

---

### T04 — Gate 1: E2E thin slice (minimální board)

* **Owner:** UI
* **Timebox:** 45 min
* **Inputs:** API kontrakt + šablony
* **Outputs:** Kanban UI + endpoint “move card” + DB persist + HTMX refresh
* **Evidence:** ve videu přesuneš kartu a hned vidíš změnu
* **Prompt:**

  > Implementuj minimální board: listy vedle sebe, karty, vytvoření karty, přesun mezi listy (HTMX/Sortable). Přesun musí volat API a uložit DB. Neřeš design, řeš stabilitu a čitelnost.

---

### T05 — Audit log jako “páteř důvěry”

* **Owner:** SRE
* **Timebox:** 35 min
* **Inputs:** doménové eventy ze SPEC
* **Outputs:** audit middleware + helper pro doménové eventy + `/ui/audit`
* **Evidence:** po přesunu karty je v audit logu `card_moved` s request id
* **Prompt:**

  > Přidej audit logging: každý request má correlation/request id; doménové akce zapisují audit_event (actor=“system” pro MVP). Ukaž audit v UI (tabulka, filtrování podle typu). Zapiš audit na: card_created, card_moved.

---

### T06 — Gate 2: Monitoring minimum

* **Owner:** SRE
* **Timebox:** 25 min
* **Inputs:** běžící appka
* **Outputs:** `/health`, `/metrics` (text), základní request logging (request id)
* **Evidence:** curl na `/metrics` ukáže counters; demo “tohle je ops-ready”
* **Prompt:**

  > Přidej /health (ok:true). Přidej /metrics v Prometheus text formátu: request_count, error_count, open_incidents, open_high_alerts. Zajisti, že audit a logy nesou request id.

---

### T07 — Gate 3: Alerts + watcher eskalace + incident timeline

* **Owner:** SRE
* **Timebox:** 50 min
* **Inputs:** doménové eventy, audit
* **Outputs:** Alerts UI + incidents UI + `scripts/watcher.py` + incident timeline + audit `alert_escalated`
* **Evidence:** “vytvořím high alert → watcher sám vytvoří incident”
* **Prompt:**

  > Implementuj alerty (create/list). Implementuj incidenty (create via escalation, list, detail s timeline). Napiš watcher.py: polluje DB každých X s a eskaluje high/critical alerty starší než Y sekund. Při eskalaci vytvoř incident + incident_event + audit_event.

---

### T08 — DR: Backup/restore jako “ops flex”

* **Owner:** SRE
* **Timebox:** 35 min
* **Inputs:** DB schéma
* **Outputs:** `scripts/backup.py`, `scripts/restore.py` + audit `backup_created`/`restore_applied`
* **Evidence:** v demu pustíš backup skript a ukážeš vznik souboru + audit event
* **Prompt:**

  > Implementuj backup.py: vytvoří timestamped snapshot (např. JSON export) a zapíše audit_event. Implementuj restore.py: aplikuje snapshot transakčně a zapíše audit_event. Přidej stručné instrukce do README.

---

### T09 — Gate 4: Agent proof (triage + remediation tasks)

* **Owner:** AI
* **Timebox:** 45 min
* **Inputs:** incident data + tools, audit
* **Outputs:** `scripts/agent.py` (summarize + propose tasks), fallback bez LLM, audit `agent_ran`, vytvořené karty v “Remediation” listu
* **Evidence:** spustíš `python scripts/agent.py summarize --incident-id 1` a `propose-tasks` a v UI se objeví nové karty
* **Prompt:**

  > Napiš agent.py s příkazy: summarize(incident) a propose-tasks(incident). Pokud je dostupný LLM key, použij; jinak rule-based fallback. propose-tasks musí vložit 3–7 karet do listu “Remediation” a zapsat audit_event agent_ran s výsledkem.

---

### T10 — MCP-ready /tools katalog (strategický signál)

* **Owner:** AI
* **Timebox:** 20 min
* **Inputs:** existující API akce
* **Outputs:** endpoint `/tools` popisující dostupné akce + `/docs/MCP_READY.md`
* **Evidence:** porota vidí “připravené na rozšíření” bez keců
* **Prompt:**

  > Přidej /tools endpoint, který vrací JSON katalog akcí (např. create_card, move_card, create_alert, close_incident) včetně jednoduchého input schema. Sepiš MCP_READY.md: jak by se to mapovalo na tool-calls agentů.

---

### T11 — BDD implementace a testy (musí být zelené)

* **Owner:** QA
* **Timebox:** 45 min
* **Inputs:** features + API
* **Outputs:** pytest-bdd step definitions + smoke testy pro /health a klíčové flows
* **Evidence:** v demu pustíš `pytest` a je zeleno
* **Prompt:**

  > Implementuj step definitions pro feature scénáře. Minimalizuj flaky věci: testuj přes API + DB. Přidej smoke test /health a “create alert → run escalation function once” (může být helper místo reálného pollu).

---

### T12 — REVIEW: Human-made pass + code review

* **Owner:** REVIEW
* **Timebox:** 25 min
* **Inputs:** celý kód + docs
* **Outputs:** PR/commit s refaktorem (názvy, struktura), odstranění “AI smell”, zkrácení README na to, co porota potřebuje
* **Evidence:** repo vypadá jako inženýrská práce, ne generovaný guláš
* **Prompt:**

  > Udělej code review: najdi 10 největších míst, kde to vypadá “AI-generated” (nekonzistentní názvy, duplikace, dlouhé funkce). Navrhni konkrétní refaktory a proveď je. Udrž to čitelné a explicitní.

---

### T13 — Demo Producer: Video scénář + záběry + 1-pager

* **Owner:** ORCH (nebo samostatně)
* **Timebox:** 35 min
* **Inputs:** běžící app, gates hotové
* **Outputs:** `/docs/DEMO.md` (2–4 min), `/docs/ONEPAGER.md` (1 stránka), checklist záběrů
* **Evidence:** porota pochopí systém do 90 sekund
* **Prompt:**

  > Sepiš demo script: 1) intro “ekosystém” (app + watcher + agent), 2) ukaž BDD (feature + pytest), 3) use-case flow (task→alert→incident→agent→tasks), 4) ops (metrics + backup). Napiš 1stránkový popis: co to je, proč, jak spustit, jaké jsou ops prvky.

---

### T14 — Release: Tag + odevzdací balík

* **Owner:** ORCH
* **Timebox:** 20 min
* **Inputs:** repo, URL (pokud deployneš), docs
* **Outputs:** release tag, `CHANGELOG.md`, `/docs/SUBMISSION.md` (text emailu + odkazy)
* **Evidence:** “release proces” splněn viditelně
* **Prompt:**

  > Připrav release: semver tag (v0.1.0), changelog, submission.md s checklistem: repo URL, demo video link, běžící URL (pokud je), co porota má zkontrolovat.

---

## E) 5 hodin: doporučené časové bloky (maximalizace “gate completion”)

* **0:00–0:35** T00 + T01 + T02 (procesní základ; paralelně v agentech)
* **0:35–1:40** T03 + T04 (Gate 1 hotový co nejdřív)
* **1:40–2:40** T05 + T06 (Gate 2)
* **2:40–3:50** T07 (Gate 3)
* **3:50–4:35** T08 + T09 (Gate 4)
* **4:35–5:00** T11 + T12 + T13 + T14 (zelené testy + demo + odevzdání)

Tohle pořadí není názor. Je to optimalizace: **nejdřív důkazy, potom polish**.

---

## F) Praktická “operace” v AI-IDE (aby agenti nepsali proti sobě)

* **Jedno vlákno pro ORCH:** jen rozhodnutí a priority.
* **Každý ticket = samostatná větev** (nebo aspoň samostatný commit blok).
* **Po každém gate:** krátký “Judge Simulation” (REVIEW): *co bych jako hodnotitel shodil?*
* **Nedělej více UI než je nutné pro demo backbone.** “Hezké” UI není bodovací kritérium.

---

## G) Zakomponované “skills” (v tomhle workflow jsou přímo zabudované)

* **Spec/BDD:** T01 + T02 + T11 (důkaz `.feature` + zelené testy)
* **Monitoring/SRE:** T06 (metrics/health/logs)
* **Incident response:** T07 (watcher → incident + timeline)
* **Audit & security mindset:** T05 + audit eventy napříč
* **DR:** T08 (backup/restore skripty)
* **AI agents & tool readiness:** T09 + T10 (`agent.py` + `/tools`)
* **Release:** T14 (tag + changelog + submission pack)
* **Human-made:** T12 (refactor pass)

---


