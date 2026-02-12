Jasně. Níže máš **workflow pro rozhodování** (ne pro programování) navržený tak, jak by ho v roce 2026 dělali lidi, co vyhrávají podobné “5 hodin / demo / agenti” challenge. Je to postavené na tom, že vyhraješ hlavně **správnou volbou řezu, důkazů a prezentace**, ne “nejvíc featur”.

Budu používat pojem **artefakt** = cokoliv, co jde ukázat hodnotitelům (repo, URL, demo video, 1-pager, testy, audit log, metrics, release tag…).

---

## Strategický workflow pro rozhodování, co dělat dál

### 1) Rozbal rubricu na “bodovací mapu”

**Cíl rozhodnutí:** vědět, co přesně maximalizuje skóre (a co je jen hezké, ale nehodnotí se).
**Vstupy:** text zadání + hodnoticí kritéria.
**Výstupy (artefakty):**

* “Score Map” = tabulka kritérií → jaký důkaz to prokazuje (konkrétní artefakt).
* Váhy (např. 1–5) podle toho, jak explicitně je to v zadání a jak snadno se to dá ověřit z videa/URL.
  **Zdůvodnění:** Hodnotitelé netelepatizují. Co neuvidí během 2–3 minut, to jako by nebylo.

Prakticky: každé kritérium musí mít *důkaz* typu “otevřu stránku / endpoint / soubor a hned to vidím”.

---

### 2) Z toho udělej “Winning Narrative” (příběh dema)

**Cíl rozhodnutí:** určit jednu větu, která spojuje všechno do srozumitelného příběhu.
**Vstupy:** Score Map.
**Výstupy:**

* 1 věta “příběhu” (např. “Alert vznikne → eskaluje na incident → agent navrhne kroky → vzniknou tasky → vše je auditované a měřené”).
* “Demo Backbone” = 5–7 kroků, které v demu projdeš vždy, i kdyby padaly ostatní věci.
  **Zdůvodnění:** V 5 hodinách vyhrává ten, kdo má demo, které působí nevyhnutelně (každý krok logicky navazuje).

---

### 3) Hard constraints rozhodnutí (platforma, perzistence, čas)

**Cíl rozhodnutí:** odstranit slepé uličky dřív, než se do nich pustíš.
**Vstupy:** požadavek na URL, jednoduchost pro laiky, čas 5h, preference deploy (např. Vercel), nutnost audit/DR/monitoring.
**Výstupy:**

* “Constraints memo” (max 10 řádků): co je zakázané/nevhodné (např. long-running procesy, lokální FS jako zdroj pravdy).
* “Platform decision” + 2–3 věty proč.
  **Zdůvodnění:** Nejvíc času se v těchto challenge pálí na nekompatibility platformy, které se projeví až pozdě.

---

### 4) Volba “thin-slice” řezu pomocí scoring funkce (value/effort/risk)

**Cíl rozhodnutí:** vybrat nejmenší průchod systémem, který najednou dokazuje co nejvíc kritérií.
**Vstupy:** Winning Narrative + Constraints + Score Map.
**Výstupy:**

* 3 kandidátní řezy (A/B/C) a rychlé skóre:

  * **Coverage**: kolik kritérií to prokazuje
  * **Demo clarity**: jak snadno to pochopí laik
  * **Build risk**: co se může rozbít
  * **Time cost**: odhad v blocích 30 min
* Výběr 1 řezu + jasně napsané “co vědomě zahazuju”.
  **Zdůvodnění:** To není “produktové plánování”, to je optimalizace na výhru. Vyhraje ten, kdo má nejvyšší *coverage/čas*.

---

### 5) Nastavení “gates” (rozhodovací brány) – aby ses neutopil

**Cíl rozhodnutí:** mít body, kde se stopneš a zhodnotíš, jestli pokračovat, nebo seškrtat scope.
**Vstupy:** vybraný thin-slice + čas.
**Výstupy:**

* 4 brány s tvrdým “go/no-go”:

  1. **E2E průchod existuje** (UI→API→DB→nějaký log/metric)
  2. **Důkaz SRE existuje** (health/metrics + základ incident flow)
  3. **Důkaz DR existuje** (backup+restore + audit stopa)
  4. **Důkaz agentů existuje** (agent něco udělá + je to dohledatelné)
* Každá brána má “když nejde, fallback”: co dropneš.
  **Zdůvodnění:** V časovém limitu není největší riziko “nemít funkce”, ale “mít rozdělané všechno a hotové nic”.

---

### 6) Multiagentní rozhodovací smyčka (ne jen generování kódu)

Tady je to “2026 způsob”: agenti nejsou jen implementátoři, ale i **rozhodovací orgány**.

#### Role agentů a jejich rozhodovací výstupy

* **Orchestrator**: drží Score Map, gates, čas. Vydává “priority order” na další 30–60 min blok.
* **Architect**: navrhuje 1–2 varianty designu, hodnotí dopady na audit/DR/monitoring.
* **QA/BDD**: definuje “co je pravda” přes scénáře; říká “hotovo/není hotovo”.
* **SRE**: hlídá observability a incident flow; stopuje věci, co nejsou měřitelné.
* **Security/Audit**: hlídá audit stopu a determinismus.
* **Demo Producer**: hlídá, že každý nový prvek přidává něco do videa/1-pageru.
* **Red Team Reviewer**: hledá, jak by to hodnotitel shodil (“tohle je fake”, “tohle nejde ověřit”, “tohle nedává smysl”).

**Cíl rozhodnutí:** každá práce musí projít “agent review”, jinak se nepočítá jako progress.
**Vstupy:** změna (PR/commit/feature), gates.
**Výstupy:** krátké verdicty: “ship / fix / drop”.

**Zdůvodnění:** Hodnotitelé milují, když je vidět proces: specifikace → test → implementace → měření → audit → release.

---

### 7) “Evidence-first” pravidlo: nic nedělat, dokud není definovaný důkaz

**Cíl rozhodnutí:** aby každý krok produkoval ukazatelný artefakt.
**Vstupy:** backlog věcí, Score Map.
**Výstupy:** pro každý krok jedna věta: “Jak to hodnotitel uvidí?” (soubor/URL/screen v demu).
**Zdůvodnění:** Spousta lidí dělá věci, které jsou “správné”, ale nejsou vidět. To je v soutěži ekvivalent nulového bodu.

---

### 8) “Stop doing list” – aktivní obrana proti feature creep

**Cíl rozhodnutí:** chránit demo a doručení.
**Vstupy:** nové nápady během práce.
**Výstupy:** živý seznam “neděláme” + podmínky, kdy by se to přehodnotilo (téměř nikdy).
**Zdůvodnění:** Největší nepřítel výhry je vlastní kreativita ve špatný čas.

---

### 9) Finalizační rozhodnutí: prezentace je součást produktu

**Cíl rozhodnutí:** rozhodnout, kdy přestat stavět a začít balit.
**Vstupy:** gates splněné? demo backbone funguje? CI zelená?
**Výstupy:** “Freeze time” (např. posledních 45–60 min) věnovaný jen:

* demo script + video take
* 1-pager
* release tag + checklist odevzdání
  **Zdůvodnění:** Hodnotitelé porovnávají *artefakt balíček*, ne tvůj vnitřní pocit, že “ještě bych to dodělal”.

---

## Jedna věc navíc, která reálně zvyšuje šanci na výhru

**“Judge Simulation” checkpoint (15 min)**
Red Team agent dostane jen to, co uvidí hodnotitel: URL + repo + 1-pager (bez tvých vysvětlení) a sepíše:

* 3 největší pochybnosti (“tohle vypadá jako fake / nedůvěryhodné / nepochopitelné”)
* 3 nejrychlejší opravy pro zlepšení důvěryhodnosti

Tohle je brutálně účinné, protože tě to donutí optimalizovat na realitu hodnotitele, ne na vlastní představu.

---

Tímhle workflowem se rozhoduješ tak, aby každých 30–60 minut přibyly **ověřitelné důkazy** pro rubriku a současně sis hlídal, že na konci existuje **příběh**, který jde natočit a odevzdat.

Další logický krok po tomhle (až budeš chtít) je převést Score Map + gates do konkrétní “agent task tabule” (prompty pro agenty + očekávané artefakty + deadline bloky), aby to šlo rovnou nalít do Cursor / Windsurf / Microsoft Visual Studio Code a jet.
