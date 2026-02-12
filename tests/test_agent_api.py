from __future__ import annotations

from app.services.llm_gemini import LLMUnavailable


def _create_incident(fake_db):
    alert = fake_db.create_alert("DB latency", "high", "test")
    return fake_db.create_incident_from_alert(alert)


def test_agent_run_uses_llm(monkeypatch, client, fake_db):
    incident = _create_incident(fake_db)

    def fake_generate_text(prompt: str, *, thinking_level: str = "minimal") -> str:
        if "odrazky" in prompt:
            return "- Restart service\n- Scale workers\n- Confirm error budget"
        return "Triage summary from Gemini mock."

    monkeypatch.setattr("app.services.agent.generate_text", fake_generate_text)
    response = client.post(f"/api/agent/run?incident_id={incident['id']}&mode=both")
    assert response.status_code == 200
    body = response.json()
    assert body["llm_used"] is True
    assert body["llm_model"] == "gemini-3-flash-preview"
    assert len(body["task_ids"]) >= 1

    agent_events = [e for e in fake_db.audit_events if e["action"] == "agent_ran"]
    assert len(agent_events) == 1
    assert agent_events[0]["payload"]["llm_used"] is True
    assert agent_events[0]["payload"]["llm_model"] == "gemini-3-flash-preview"


def test_agent_run_fallback_when_llm_unavailable(monkeypatch, client, fake_db):
    incident = _create_incident(fake_db)

    def fail_generate_text(prompt: str, *, thinking_level: str = "minimal") -> str:
        raise LLMUnavailable("mock unavailable")

    monkeypatch.setattr("app.services.agent.generate_text", fail_generate_text)
    response = client.post(f"/api/agent/run?incident_id={incident['id']}&mode=both")
    assert response.status_code == 200
    body = response.json()
    assert body["llm_used"] is False
    assert len(body["task_ids"]) >= 1

    agent_events = [e for e in fake_db.audit_events if e["action"] == "agent_ran"]
    assert len(agent_events) == 1
    assert agent_events[0]["payload"]["llm_used"] is False
