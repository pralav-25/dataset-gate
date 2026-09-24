def test_baseline_promotion(client):
    report = client.post(
        "/api/v1/validate",
        json={
            "csv": "id\na",
            "contract": {
                "version": 1,
                "name": "x",
                "rules": [{"id": "u", "check": "unique", "column": "id"}],
            },
            "save": True,
        },
    ).json()
    body = {"name": "release", "run_id": report["run_id"]}
    assert client.post("/api/v1/baselines", json=body).status_code == 200
    assert client.post("/api/v1/baselines", json=body).status_code == 400
    assert client.get("/api/v1/baselines").json() == [body]
