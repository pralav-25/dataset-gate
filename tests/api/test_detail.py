def test_saved_detail(client):
    body = {
        "csv": "id\na",
        "contract": {
            "version": 1,
            "name": "x",
            "rules": [{"id": "u", "check": "unique", "column": "id"}],
        },
        "save": True,
    }
    report = client.post("/api/v1/validate", json=body).json()
    response = client.get("/api/v1/runs/" + report["run_id"])
    assert response.json()["report"] == report
    assert client.get("/api/v1/runs/missing").status_code == 404
