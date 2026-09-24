def test_report_download(client):
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
    response = client.get("/api/v1/runs/" + report["run_id"] + "/report")
    assert response.status_code == 200 and "text/html" in response.headers["content-type"]
    assert "Dataset Gate" in response.text
    assert client.get("/api/v1/runs/missing/report").status_code == 404
