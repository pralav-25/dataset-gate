"""The uuid rule is usable through the public validation endpoint."""


def test_uuid_validation_and_catalog(client):
    contract = {
        "version": 1,
        "name": "uuid integration",
        "rules": [{"id": "uuid", "check": "uuid", "params": {}, "column": "value"}],
    }
    response = client.post(
        "/api/v1/validate",
        json={"csv": "value\n550e8400-e29b-41d4-a716-446655440000\nbad", "contract": contract},
    )
    assert response.status_code == 200
    finding = response.json()["results"][0]
    assert finding["check"] == "uuid" and finding["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "uuid" for rule in catalog)
    contract["rules"][0]["params"]["unknown"] = 1
    assert (
        client.post(
            "/api/v1/validate",
            json={"csv": "value\n550e8400-e29b-41d4-a716-446655440000\nbad", "contract": contract},
        ).status_code
        == 400
    )
