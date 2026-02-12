from pytest_bdd import given, parsers, scenario, then, when


@scenario("features/card_move_audit.feature", "Move card to In Progress")
def test_card_move_creates_audit():
    pass


@scenario("features/high_alert_incident.feature", "High alert escalates to incident")
def test_high_alert_escalates():
    pass


@given("a card exists in Todo", target_fixture="card_id")
def given_card_exists(fake_db):
    card = fake_db.create_card("Card A", "desc", "Todo")
    return card["id"]


@when("I move the card to In Progress")
def when_move_card(client, card_id):
    response = client.post(
        f"/cards/{card_id}/move", data={"column_name": "In Progress"}, follow_redirects=False
    )
    assert response.status_code == 303


@then("an audit event card_moved is recorded")
def then_audit_recorded(fake_db):
    actions = [e["action"] for e in fake_db.audit_events]
    assert "card_moved" in actions


@given("a high alert exists")
def given_high_alert(fake_db):
    fake_db.create_alert("CPU above 95%", "high", "test")


@when("I run the watcher once")
def when_run_watcher(client):
    response = client.post("/watcher/run-once", follow_redirects=False)
    assert response.status_code == 303


@then(parsers.parse("{count:d} incident is created"))
def then_incident_created(fake_db, count):
    assert len(fake_db.incidents) == count
