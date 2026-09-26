"""Verify not_in through public validation and rule-discovery endpoints."""


def test_validation_catalog_and_malformed_contract(client):
    contract = {
        "version": 1,
        "name": "not_in integration",
        "rules": [
            {"id": "rule", "check": "not_in", "column": "value", "params": {"values": ["unknown"]}}
        ],
    }
    csv = "value\nvalid\nunknown"
    response = client.post("/api/v1/validate", json={"csv": csv, "contract": contract})
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["check"] == "not_in" and result["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "not_in" for rule in catalog)
    contract["rules"][0]["params"]["typo"] = 1
    assert (
        client.post("/api/v1/validate", json={"csv": csv, "contract": contract}).status_code == 400
    )
