# AI Code Review (Top 10 Risks + Fixes)

1. **High:** RLS disabled on demo tables.
   - Fix: zavést auth + RLS policies per user/team.
2. **High:** `/watcher/run-once` je veřejně volatelné.
   - Fix: přidat token auth nebo interní scheduler only.
3. **High:** DR import přepisuje data bez potvrzení/verze.
   - Fix: dry-run validace + backup before import.
4. **Medium:** `DataAccess.import_all` maže celé tabulky.
   - Fix: transaction + scoped restore mode.
5. **Medium:** `/metrics` každé volání čte DB counts.
   - Fix: cache 10-30s nebo async background snapshot.
6. **Medium:** Agent fallback vrací statické tasky.
   - Fix: přidat kontextové generování podle incident timeline.
7. **Medium:** Chybí retry/backoff při Supabase chybách.
   - Fix: wrap DB calls s retry politikou.
8. **Low:** UI nemá CSRF ochranu.
   - Fix: CSRF token middleware.
9. **Low:** Chybí pagination na audit page.
   - Fix: limit/offset + filtry.
10. **Low:** Chybí e2e test pro DR export/import.
   - Fix: přidat BDD scénář restore workflow.

## Conscious tradeoffs
- Priorita byla doručit challenge MVP ve 5h.
- Proto minimal auth/security a jednodušší watcher/agent orchestrace.
