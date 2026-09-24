def test_history_filters_and_limits(client):
    assert client.get("/api/v1/runs").json()["total"] == 0
    assert client.get("/api/v1/runs?limit=201").status_code == 422
    assert client.get("/api/v1/runs?status=unknown").status_code == 400
