# Vercel Login Troubleshoot (Black Screen)

Cil: 5 minutovy fix loop, ne dlouhe ladeni.

1. Otevri `https://vercel.com/login` v anonymnim okne (Chrome/Edge) a zkus login pres GitHub.
2. Docasne vypni adblock/privacy rozsireni (`uBlock`, `AdBlock`, `PrivacyBadger`, `Ghostery`) a dej refresh.
3. Vymaz site data jen pro `vercel.com` (Chrome: Site settings -> Clear data).
4. Povol cookies (vcetne third-party pro `vercel.com` + `github.com`) a zkus znovu.
5. Vypni VPN/proxy, nebo zkus hotspot.
6. Zkus jiny prohlizec (Chrome <-> Edge <-> Firefox).

Pokud to stale nejde:
- Nepodminuj submission dashboardem.
- Pouzij no-dashboard postup z `docs/AI_PROOF.md` a `docs/SUBMISSION_FINAL_CHECKLIST.md`.
