from __future__ import annotations

import json
from typing import Any
from sqlalchemy.orm import Session

from .models import AuditEvent
from .metrics import domain_events_total

def log_event(
    db: Session,
    *,
    actor: str,
    action: str,
    entity_type: str,
    entity_id: str,
    correlation_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    domain_events_total.labels(action=action).inc()
    ae = AuditEvent(
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        correlation_id=correlation_id,
        details_json=json.dumps(details or {}, ensure_ascii=False),
    )
    db.add(ae)
    db.commit()
