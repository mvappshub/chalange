from __future__ import annotations

from pytest_bdd import given, when, then, scenarios
from fastapi.testclient import TestClient

from app.main import app

scenarios("../features/move_card_audit.feature")

client = TestClient(app)

@given("I have the default board")
def default_board():
    r = client.get("/api/boards/default")
    assert r.status_code == 200
    return r.json()

@given('I create a card in list "Backlog"')
def create_card(default_board):
    backlog = next(l for l in default_board["lists"] if l["name"] == "Backlog")
    r = client.post("/api/cards", json={"title": "Test card", "description": "x", "list_id": backlog["id"]})
    assert r.status_code == 200
    return {"card_id": r.json()["id"], "backlog_id": backlog["id"], "board": default_board}

@when('I move the card to list "In Progress"')
def move_card(create_card):
    inprog = next(l for l in create_card["board"]["lists"] if l["name"] == "In Progress")
    r = client.post(f"/api/cards/{create_card['card_id']}/move", json={"list_id": inprog["id"]})
    assert r.status_code == 200
    return True

@then('audit contains action "card_moved"')
def audit_contains():
    r = client.get("/api/audit?limit=200")
    assert r.status_code == 200
    actions = [x["action"] for x in r.json()]
    assert "card_moved" in actions
