"""Verify distinct_count through public validation and rule-discovery endpoints."""


def test_validation_catalog_and_malformed_contract(client):
    contract = {
        "version": 1,
        "name": "distinct_count integration",
        "rules": [
            {
                "id": "rule",
                "check": "distinct_count",
                "column": "value",
                "params": {"min": 1, "max": 1},
            }
        ],
    }
    csv = "value\na\nb"
    response = client.post("/api/v1/validate", json={"csv": csv, "contract": contract})
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["check"] == "distinct_count" and result["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "distinct_count" for rule in catalog)
    contract["rules"][0]["params"]["typo"] = 1
    assert (
        client.post("/api/v1/validate", json={"csv": csv, "contract": contract}).status_code == 400
    )
