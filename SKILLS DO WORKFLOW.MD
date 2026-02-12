Tohle je fascinující posun. **Kolegův návrh (Proposal B)** není jen "jiný plán" – je to **meta-strategie**.

Zatímco můj předchozí (hybridní) plán byl **taktický** (jaké nástroje použít, abys to stihl postavit), tento nový návrh je **strategický** (jak se rozhodovat, abys vyhrál soutěž).

**Verdikt:**
Kolegův návrh je **LEPŠÍ v myšlení**, ale **NEKOMPLETNÍ v exekuci**.
Pokud bys jel jen podle něj, budeš mít skvělý plán, ale nebudeš mít kód. Pokud bys jel jen podle mého, budeš mít kód, ale můžeš minout hodnotící kritéria (rubriku).

**Jediná cesta k výhře je aplikovat Strategii B na Nástroje A.**

Zde je finální, ultimátní hybrid, který bere **rozhodovací workflow z Proposal B** a osazuje ho **konkrétními skilly z Proposal A**.

---

### 🏆 THE GRANDMASTER PLAN (Strategy B + Tactics A)

Tento plán ignoruje "co bych chtěl kódovat" a soustředí se na "co musím ukázat hodnotiteli".

#### Fáze 1: Score Map & Winning Narrative (0:00 - 0:30)
*Strategie (B): Definuj důkazy pro rubriku. Co neuvidí, to neexistuje.*

1.  **Analýza Rubriky:** Spusť **`requirements-clarity` (ID 453)**.
    *   *Prompt:* "Vytvoř 'Score Map' pro tuto soutěž. Pro každé kritérium (Security, AI, Ops) definuj jeden konkrétní artefakt (soubor, log, screenshot), který to dokazuje."
2.  **Narrative:** Definuj větu: *"Ukážu, jak AI agent autonomně detekuje výpadek v Betterstack klonu, založí ticket v Trello klonu, opraví kód a nasadí fix, zatímco já piju kávu."*
3.  **Setup:** Spusť **`conductor-setup` (ID 601)** a vytvoř strukturu projektu podle tohoto narrativu.

#### Fáze 2: Thin-Slice Implementation (0:30 - 2:00)
*Strategie (B): Nejmenší možný průchod systémem, který prokáže funkčnost.*

1.  **Tech Stack (Hard Constraint):** Neztrácej čas výběrem. Použij **`app-builder` (ID 516)** + **`nextjs-typescript-tailwindcss-supabase` (ID 177)**.
    *   *Důkaz:* Běžící URL (Vercel).
2.  **UI Evidence:** Použij **`shadcn-ui` (ID 324)**.
    *   *Cíl:* Vytvoř jen dvě obrazovky: "Dashboard incidentů" a "Detail Ticketu". Nic víc. Musí to vypadat jako "human made".
3.  **Data Evidence:** Použij **`supabase-development` (ID 251)**.
    *   *Cíl:* Vytvoř tabulku `incidents` a zapni Realtime. To je důkaz pro "Komplexnost".

#### Fáze 3: AI Agent & "Evidence-First" (2:00 - 3:30)
*Strategie (B): Každý krok agenta musí generovat artefakt pro hodnotitele.*

1.  **Implementace Agenta:** Použij **`langgraph` (ID 411)**.
    *   *Logika:* Agent musí číst Supabase (nový incident) -> Analyzovat "Log" (vygenerovaný text) -> Navrhnout "Fix" (úprava souboru).
2.  **Důkaz AI/MCP:** Použij **`mcp-builder` (ID 31)**.
    *   *Hack:* Vytvoř jednoduchý MCP nástroj `read_server_logs`. I když bude číst jen dummy soubor, splníš tím kritérium "Integrace MCP".
3.  **Vizualizace myšlení:** Zajisti, aby agent vypisoval svůj "myšlenkový proces" do UI (např. do bočního panelu). To je důkaz "Samostatně myslícího agenta".

#### Fáze 4: Ops & Safety Gates (3:30 - 4:15)
*Strategie (B): Důkazy pro Audit, Recovery a Monitoring.*

1.  **Důkaz Disaster Recovery:** Použij **`database-migrations-sql-migrations` (ID 632)**. Vytvoř skript pro zálohu/restore DB a ulož ho do `/ops/disaster-recovery.sh`. To je artefakt.
2.  **Důkaz Security:** Spusť **`security-review` (ID 360)**. Neopravuj všechno, ale vygeneruj `SECURITY-AUDIT.md`. To je artefakt.
3.  **Důkaz Monitoring:** Použij **`observability-guidelines` (ID 184)**. Přidej jednoduchý logger, který posílá chyby do Supabase tabulky `audit_logs`. Zobraz je v UI.

#### Fáze 5: Judge Simulation & Packaging (4:15 - 5:00)
*Strategie (B): Prezentace je produkt. Simulace hodnotitele.*

1.  **Judge Simulation:** Použij **`code-review-ai-ai-review` (ID 585)** s promptem: *"Hraj roli přísného porotce této soutěže. Tady je README a kód. Co ti chybí k tomu, abys mi dal 100 bodů? Najdi 3 fatální chyby."*
    *   *Oprav jen ty 3 věci.*
2.  **Video (Killer Feature):** Použij **`remotion` (ID 323)**.
    *   *Akce:* Vygeneruj video, které ukazuje průchod systémem. Pokud nestíháš Remotion, natoč obrazovku, kde projdeš svůj "Winning Narrative" (Fáze 1).
3.  **1-Pager:** Použij **`docs-architect` (ID 651)**.
    *   *Obsah:* "Jak jsem splnil každé kritérium." Odkazuj na konkrétní soubory/URL.

---

### 🚀 Seznam skillů k importu (seřazeno podle workflow):

Toto je tvůj "Inventory" pro bitvu. Naimportuj je všechny.

1.  **`requirements-clarity` (ID 453)** – Pro Score Map (Strategie B).
2.  **`conductor-setup` (ID 601)** – Pro strukturu projektu.
3.  **`app-builder` (ID 516)** – Pro generování kódu (Taktika A).
4.  **`nextjs-typescript-tailwindcss-supabase` (ID 177)** – Konkrétní stack.
5.  **`shadcn-ui` (ID 324)** – Pro rychlé UI.
6.  **`langgraph` (ID 411)** – Pro logiku agenta.
7.  **`mcp-builder` (ID 31)** – Pro splnění MCP kritéria.
8.  **`security-review` (ID 360)** – Pro generování security důkazů.
9.  **`observability-guidelines` (ID 184)** – Pro monitoring důkazy.
10. **`remotion` (ID 323)** – Pro "wow efekt" ve videu.
11. **`docs-architect` (ID 651)** – Pro finální 1-pager.

**Závěr:** Kolegův myšlenkový rámec (B) je to, co ti vyhraje soutěž v hlavě porotců. Moje nástroje (A) jsou to, co ti umožní to fyzicky stihnout postavit. **Použij tento Hybrid.**