# OpsBoard Design System Master

> Logic: check `design-system/pages/[page].md` first. If it exists, page rules override this Master file. If it does not exist, follow this file only.

## Target Category
- Product: Developer Tools / AI Platform / Real-Time Monitoring dashboard
- Visual direction: AI-native, clean, minimalist, high readability
- Theme: OLED dark with subtle borders and dimensional layering
- Layout language: bento cards for status and metrics

## Core Tokens
- `--bg`: `#06090f`
- `--surface`: `#0f1622`
- `--surface-2`: `#121d2d`
- `--border`: `#243248`
- `--text`: `#e8eef8`
- `--muted`: `#98a8bf`
- `--primary`: `#5ac8fa`
- `--danger`: `#ef4444`
- `--warning`: `#f59e0b`
- `--success`: `#22c55e`

## Typography
- Heading/body font: modern sans (`IBM Plex Sans` fallback stack)
- Technical content font: monospace (`JetBrains Mono` fallback stack)
- Body minimum: 16px equivalent on mobile
- Line height: 1.5-1.6 for readability

## Layout Rules
- Top navigation always visible and compact.
- Main content max width: 1100-1200px.
- Spacing scale: 4/8/12/16/20/24/32px.
- Use rounded cards with subtle borders and soft shadows.
- Keep dense data in tables with sticky headers and row hover.

## Component Rules
- Buttons: one visual family, variants = primary, secondary, ghost, danger.
- Badges: use color-coded severity and status pills.
- Callouts: green success callout for completed escalation/restore feedback.
- Code blocks: monospace, bounded height, scrollable.
- Forms: labels + visible focus ring.

## Motion + Interaction
- Micro-interactions only (150-250ms).
- Use border/shadow/translateY hover for cards and buttons.
- Never use heavy transforms that shift layout.
- Respect `prefers-reduced-motion`.

## Accessibility Baseline
- Keep contrast in dark mode at readable levels.
- Visible keyboard focus on all interactive controls.
- Clickable controls must show pointer cursor and hover state.
- Use color + text/badge labels, not color alone.

## Design Principles
1. Clarity over decoration.
2. Status at a glance.
3. Consistent interaction language.
4. Dense data, low cognitive load.
5. Safe defaults for destructive flows.
