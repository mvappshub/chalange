from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from supabase import Client, create_client

from app.config import get_settings


class DataAccess:
    def __init__(self, client: Client):
        self.client = client

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def list_cards(self) -> list[dict[str, Any]]:
        response = self.client.table("cards").select("*").order("created_at").execute()
        return response.data or []

    def create_card(self, title: str, description: str, column_name: str = "Todo") -> dict[str, Any]:
        row = {
            "id": str(uuid4()),
            "title": title,
            "description": description,
            "column_name": column_name,
            "created_at": self._now(),
            "updated_at": self._now(),
        }
        inserted = self.client.table("cards").insert(row).execute().data[0]
        self.create_audit_event("card_created", "card", inserted["id"], {"column_name": column_name})
        return inserted

    def move_card(self, card_id: str, column_name: str) -> dict[str, Any]:
        updated = (
            self.client.table("cards")
            .update({"column_name": column_name, "updated_at": self._now()})
            .eq("id", card_id)
            .execute()
            .data[0]
        )
        self.create_audit_event("card_moved", "card", card_id, {"to_column": column_name})
        return updated

    def delete_card(self, card_id: str) -> None:
        self.client.table("cards").delete().eq("id", card_id).execute()
        self.create_audit_event("card_deleted", "card", card_id, {})

    def list_alerts(self) -> list[dict[str, Any]]:
        response = self.client.table("alerts").select("*").order("created_at", desc=True).execute()
        return response.data or []

    def create_alert(self, title: str, severity: str, source: str) -> dict[str, Any]:
        row = {
            "id": str(uuid4()),
            "title": title,
            "severity": severity,
            "source": source,
            "status": "open",
            "escalated": False,
            "created_at": self._now(),
            "updated_at": self._now(),
        }
        inserted = self.client.table("alerts").insert(row).execute().data[0]
        self.create_audit_event("alert_created", "alert", inserted["id"], {"severity": severity})
        return inserted

    def list_unescalated_high_alerts(self) -> list[dict[str, Any]]:
        response = (
            self.client.table("alerts")
            .select("*")
            .in_("severity", ["high", "critical"])
            .eq("escalated", False)
            .execute()
        )
        return response.data or []

    def mark_alert_escalated(self, alert_id: str) -> None:
        self.client.table("alerts").update({"escalated": True, "updated_at": self._now()}).eq("id", alert_id).execute()

    def list_incidents(self) -> list[dict[str, Any]]:
        response = self.client.table("incidents").select("*").order("created_at", desc=True).execute()
        return response.data or []

    def get_incident(self, incident_id: str) -> dict[str, Any] | None:
        result = self.client.table("incidents").select("*").eq("id", incident_id).limit(1).execute().data
        return result[0] if result else None

    def create_incident_from_alert(self, alert: dict[str, Any]) -> dict[str, Any]:
        row = {
            "id": str(uuid4()),
            "title": f"Incident from alert: {alert['title']}",
            "status": "investigating",
            "severity": alert["severity"],
            "source_alert_id": alert["id"],
            "summary": f"Auto escalated from {alert['severity']} alert",
            "created_at": self._now(),
            "updated_at": self._now(),
        }
        inserted = self.client.table("incidents").insert(row).execute().data[0]
        self.create_audit_event(
            "incident_created",
            "incident",
            inserted["id"],
            {"source_alert_id": alert["id"], "severity": alert["severity"]},
        )
        self.mark_alert_escalated(alert["id"])
        return inserted

    def update_incident_status(self, incident_id: str, status: str) -> None:
        self.client.table("incidents").update({"status": status, "updated_at": self._now()}).eq("id", incident_id).execute()
        self.create_audit_event("incident_status_changed", "incident", incident_id, {"status": status})

    def upsert_incident_note(self, incident_id: str, note_type: str, content: str) -> dict[str, Any]:
        existing = (
            self.client.table("incident_notes")
            .select("*")
            .eq("incident_id", incident_id)
            .eq("note_type", note_type)
            .limit(1)
            .execute()
            .data
        )
        if existing:
            updated = (
                self.client.table("incident_notes")
                .update({"content": content, "updated_at": self._now()})
                .eq("id", existing[0]["id"])
                .execute()
                .data[0]
            )
            return updated
        row = {
            "id": str(uuid4()),
            "incident_id": incident_id,
            "note_type": note_type,
            "content": content,
            "created_at": self._now(),
            "updated_at": self._now(),
        }
        return self.client.table("incident_notes").insert(row).execute().data[0]

    def list_incident_notes(self, incident_id: str) -> list[dict[str, Any]]:
        response = (
            self.client.table("incident_notes")
            .select("*")
            .eq("incident_id", incident_id)
            .order("updated_at", desc=True)
            .execute()
        )
        return response.data or []

    def list_agent_cards_for_incident(self, incident_id: str) -> list[dict[str, Any]]:
        cards = self.list_cards()
        needle = f"incident {incident_id}"
        return [card for card in cards if needle in (card.get("description") or "")]

    def create_audit_event(self, action: str, entity_type: str, entity_id: str, payload: dict[str, Any]) -> None:
        row = {
            "id": str(uuid4()),
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "payload": payload,
            "created_at": self._now(),
        }
        self.client.table("audit_events").insert(row).execute()

    def list_audit_events(self, limit: int = 100) -> list[dict[str, Any]]:
        response = self.client.table("audit_events").select("*").order("created_at", desc=True).limit(limit).execute()
        return response.data or []

    def list_audit_for_entity(self, entity_id: str) -> list[dict[str, Any]]:
        response = self.client.table("audit_events").select("*").eq("entity_id", entity_id).order("created_at").execute()
        return response.data or []

    def counts(self) -> dict[str, int]:
        tables = ["cards", "alerts", "incidents", "audit_events", "incident_notes"]
        out: dict[str, int] = {}
        for table in tables:
            count = self.client.table(table).select("id", count="exact").limit(0).execute().count or 0
            out[table] = count
        return out

    def export_all(self) -> dict[str, Any]:
        return {
            "cards": self.client.table("cards").select("*").execute().data or [],
            "alerts": self.client.table("alerts").select("*").execute().data or [],
            "incidents": self.client.table("incidents").select("*").execute().data or [],
            "audit_events": self.client.table("audit_events").select("*").execute().data or [],
            "incident_notes": self.client.table("incident_notes").select("*").execute().data or [],
        }

    def import_all(self, payload: dict[str, Any]) -> None:
        for table in ["cards", "alerts", "incidents", "audit_events", "incident_notes"]:
            self.client.table(table).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
            rows = payload.get(table, [])
            if rows:
                self.client.table(table).insert(rows).execute()


def build_data_access() -> DataAccess:
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_anon_key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_ANON_KEY are required.")
    client = create_client(settings.supabase_url, settings.supabase_anon_key)
    return DataAccess(client)
