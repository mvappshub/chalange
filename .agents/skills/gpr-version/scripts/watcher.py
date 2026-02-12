from __future__ import annotations

import time
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.settings import settings
from app.models import Alert, Severity
from app.services import create_incident
from app.db import Base
from app.audit import log_event

POLL_SECONDS = 2


def _engine():
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    return create_engine(settings.database_url, connect_args=connect_args)


def main():
    engine = _engine()
    Base.metadata.create_all(bind=engine)

    print("watcher running: polling alerts table...")
    seen: set[int] = set()

    while True:
        with Session(engine) as db:
            alerts = (
                db.execute(select(Alert).order_by(Alert.created_at.desc()).limit(50))
                .scalars()
                .all()
            )
            for a in alerts:
                if a.id in seen:
                    continue
                seen.add(a.id)

                if a.severity in (Severity.high, Severity.critical):
                    title = f"[AUTO] {a.severity.value.upper()} alert: {a.name}"
                    desc = (
                        f"source={a.source}\n"
                        f"fingerprint={a.fingerprint}\n"
                        f"message={a.message or ''}"
                    )
                    inc = create_incident(db, title, desc, a.severity, actor="watcher", corr=None)
                    log_event(
                        db,
                        actor="watcher",
                        action="alert_escalated",
                        entity_type="alert",
                        entity_id=a.id,
                        details={"incident_id": inc.id, "severity": a.severity.value},
                    )
                    print(f"{datetime.utcnow().isoformat()} escalated alert #{a.id} -> incident #{inc.id}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
