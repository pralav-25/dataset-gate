def test_quality_failure_is_a_report_not_http_error(client):
    contract = {
        "version": 1,
        "name": "Tickets",
        "rules": [{"id": "u", "check": "unique", "column": "id"}],
    }
    response = client.post(
        "/api/v1/validate", json={"csv": "id\na\na", "contract": contract, "save": True}
    )
    assert response.status_code == 200 and response.json()["status"] == "failed"
    assert response.json()["results"][0]["records"] == [2]
    assert client.post("/api/v1/validate", json={"csv": "id", "contract": {}}).status_code == 400
