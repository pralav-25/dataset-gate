"""Verify luhn through public validation and rule-discovery endpoints."""


def test_validation_catalog_and_malformed_contract(client):
    contract = {
        "version": 1,
        "name": "luhn integration",
        "rules": [{"id": "rule", "check": "luhn", "column": "value", "params": {}}],
    }
    csv = "value\n79927398713\n79927398714"
    response = client.post("/api/v1/validate", json={"csv": csv, "contract": contract})
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["check"] == "luhn" and result["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "luhn" for rule in catalog)
    contract["rules"][0]["params"]["typo"] = 1
    assert (
        client.post("/api/v1/validate", json={"csv": csv, "contract": contract}).status_code == 400
    )
