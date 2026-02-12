# Decisions

## 2026-02-12

1. **UI stack:** FastAPI + Jinja (server-rendered) bez SPA frameworku.
   - Důvod: challenge constraint, rychlost doručení, nízká komplexita.

2. **Security posture v Supabase:** `RLS OFF` na app tabulkách + explicitní granty `anon/authenticated`.
   - Důvod: veřejné demo prostředí, potřeba jednoduchého CRUD přes anon key.
   - Tradeoff: vhodné jen pro demo, ne pro produkci.

3. **Watcher režim:** implementován `--once` (CLI + endpoint `/watcher/run-once`).
   - Důvod: požadavek challenge, deterministické demo.

4. **AI agent fallback:** bez LLM klíče běží deterministický fallback.
   - Důvod: spolehlivé demo bez externích závislostí.

5. **Node launch wrapper:** přidán `package.json` se skripty, které spouští Python app (`npm run dev`).
   - Důvod: preference uživatele "spouštět přes node jak vždy".

6. **Video výstup:** dodán reprodukovatelný render skript + storyboard.
   - Důvod: v challenge čase je robustnější než závislost na plném video toolchainu.
