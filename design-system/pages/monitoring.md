# Monitoring Page Overrides

## Purpose
At-a-glance health dashboard for API, DB, watcher, and AI provider states.

## Overrides
- Use bento-style 4-card status grid as first visual block.
- Each status card includes:
  - semantic indicator color (ok/warn/bad)
  - plain-language state text
  - supporting context (timestamps/created incidents)
- Follow with compact metric cards for entity counts and HTTP metrics.
- Keep `/api/status` and `/metrics` links visible as utility actions.
