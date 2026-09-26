"""Verify unicode_normalization through public validation and rule-discovery endpoints."""


def test_validation_catalog_and_malformed_contract(client):
    contract = {
        "version": 1,
        "name": "unicode_normalization integration",
        "rules": [
            {
                "id": "rule",
                "check": "unicode_normalization",
                "column": "value",
                "params": {"form": "NFC"},
            }
        ],
    }
    csv = "value\né\né"
    response = client.post("/api/v1/validate", json={"csv": csv, "contract": contract})
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["check"] == "unicode_normalization" and result["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "unicode_normalization" for rule in catalog)
    contract["rules"][0]["params"]["typo"] = 1
    assert (
        client.post("/api/v1/validate", json={"csv": csv, "contract": contract}).status_code == 400
    )
