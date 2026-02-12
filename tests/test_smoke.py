def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "opsboard_requests_total" in response.text
