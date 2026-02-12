from __future__ import annotations

import argparse

from app.db import build_data_access


def run_once() -> int:
    db = build_data_access()
    created = 0
    for alert in db.list_unescalated_high_alerts():
        db.create_incident_from_alert(alert)
        created += 1
    db.create_audit_event("watcher_run", "system", "watcher", {"created_incidents": created})
    return created


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    if args.once:
        created = run_once()
        print(f"Watcher finished. incidents_created={created}")
        return
    print("Only --once mode is implemented for MVP.")


if __name__ == "__main__":
    main()
