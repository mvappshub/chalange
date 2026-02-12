from __future__ import annotations

from pytest_bdd import given, then, scenarios
from fastapi.testclient import TestClient

from app.main import app

scenarios("../features/alert_escalates_incident.feature")
client = TestClient(app)


@given("I create a high alert")
def create_high_alert():
    payload = {
        "name": "API error rate",
        "severity": "high",
        "source": "test",
        "message": "500s > 5%",
    }
    r = client.post("/api/alerts", json=payload)
    assert r.status_code == 200
    return r.json()


@then("the alert is stored")
def alert_stored(create_high_alert):
    assert "id" in create_high_alert
    assert "fingerprint" in create_high_alert
