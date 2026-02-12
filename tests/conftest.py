from __future__ import annotations

from datetime import datetime, timezone
from fastapi.testclient import TestClient
import uuid
import pytest

from app.main import app, get_data_access


class FakeDataAccess:
    def __init__(self):
        self.cards = []
        self.alerts = []
        self.incidents = []
        self.audit_events = []
        self.incident_notes = []

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def list_cards(self):
        return self.cards

    def create_card(self, title, description, column_name="Todo"):
        row = {"id": str(uuid.uuid4()), "title": title, "description": description, "column_name": column_name}
        self.cards.append(row)
        self.create_audit_event("card_created", "card", row["id"], {"column_name": column_name})
        return row

    def move_card(self, card_id, column_name):
        for card in self.cards:
            if card["id"] == card_id:
                card["column_name"] = column_name
                self.create_audit_event("card_moved", "card", card_id, {"to_column": column_name})
                return card
        raise KeyError(card_id)

    def delete_card(self, card_id):
        self.cards = [c for c in self.cards if c["id"] != card_id]
        self.create_audit_event("card_deleted", "card", card_id, {})

    def list_alerts(self):
        return list(reversed(self.alerts))

    def create_alert(self, title, severity, source):
        row = {
            "id": str(uuid.uuid4()),
            "title": title,
            "severity": severity,
            "source": source,
            "status": "open",
            "escalated": False,
        }
        self.alerts.append(row)
        self.create_audit_event("alert_created", "alert", row["id"], {"severity": severity})
        return row

    def list_unescalated_high_alerts(self):
        return [a for a in self.alerts if (a["severity"] in ["high", "critical"] and not a["escalated"])]

    def mark_alert_escalated(self, alert_id):
        for a in self.alerts:
            if a["id"] == alert_id:
                a["escalated"] = True

    def list_incidents(self):
        return list(reversed(self.incidents))

    def get_incident(self, incident_id):
        for i in self.incidents:
            if i["id"] == incident_id:
                return i
        return None

    def create_incident_from_alert(self, alert):
        row = {
            "id": str(uuid.uuid4()),
            "title": f"Incident from alert: {alert['title']}",
            "status": "investigating",
            "severity": alert["severity"],
            "source_alert_id": alert["id"],
            "summary": "Auto escalated",
            "created_at": self._now(),
        }
        self.incidents.append(row)
        self.create_audit_event("incident_created", "incident", row["id"], {"source_alert_id": alert["id"]})
        self.mark_alert_escalated(alert["id"])
        return row

    def upsert_incident_note(self, incident_id, note_type, content):
        for note in self.incident_notes:
            if note["incident_id"] == incident_id and note["note_type"] == note_type:
                note["content"] = content
                note["updated_at"] = self._now()
                return note
        note = {
            "id": str(uuid.uuid4()),
            "incident_id": incident_id,
            "note_type": note_type,
            "content": content,
            "created_at": self._now(),
            "updated_at": self._now(),
        }
        self.incident_notes.append(note)
        return note

    def list_incident_notes(self, incident_id):
        notes = [n for n in self.incident_notes if n["incident_id"] == incident_id]
        return sorted(notes, key=lambda x: x["updated_at"], reverse=True)

    def list_agent_cards_for_incident(self, incident_id):
        needle = f"incident {incident_id}"
        return [c for c in self.cards if needle in (c.get("description") or "")]

    def update_incident_status(self, incident_id, status):
        for i in self.incidents:
            if i["id"] == incident_id:
                i["status"] = status
        self.create_audit_event("incident_status_changed", "incident", incident_id, {"status": status})

    def create_audit_event(self, action, entity_type, entity_id, payload):
        self.audit_events.append(
            {
                "id": str(uuid.uuid4()),
                "action": action,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "payload": payload,
                "created_at": self._now(),
            }
        )

    def list_audit_events(self, limit=100):
        return list(reversed(self.audit_events))[:limit]

    def list_audit_for_entity(self, entity_id):
        return [e for e in self.audit_events if e["entity_id"] == entity_id]

    def counts(self):
        return {
            "cards": len(self.cards),
            "alerts": len(self.alerts),
            "incidents": len(self.incidents),
            "audit_events": len(self.audit_events),
            "incident_notes": len(self.incident_notes),
        }

    def export_all(self):
        return {
            "cards": self.cards,
            "alerts": self.alerts,
            "incidents": self.incidents,
            "audit_events": self.audit_events,
            "incident_notes": self.incident_notes,
        }

    def import_all(self, payload):
        self.cards = payload.get("cards", [])
        self.alerts = payload.get("alerts", [])
        self.incidents = payload.get("incidents", [])
        self.audit_events = payload.get("audit_events", [])
        self.incident_notes = payload.get("incident_notes", [])


@pytest.fixture()
def fake_db():
    return FakeDataAccess()


@pytest.fixture()
def client(fake_db):
    app.dependency_overrides[get_data_access] = lambda: fake_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
