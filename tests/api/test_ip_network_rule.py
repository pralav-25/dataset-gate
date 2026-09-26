"""Verify ip_network through public validation and rule-discovery endpoints."""


def test_validation_catalog_and_malformed_contract(client):
    contract = {
        "version": 1,
        "name": "ip_network integration",
        "rules": [
            {"id": "rule", "check": "ip_network", "column": "value", "params": {"version": "any"}}
        ],
    }
    csv = "value\n192.0.2.0/24\n192.0.2.1/24"
    response = client.post("/api/v1/validate", json={"csv": csv, "contract": contract})
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["check"] == "ip_network" and result["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "ip_network" for rule in catalog)
    contract["rules"][0]["params"]["typo"] = 1
    assert (
        client.post("/api/v1/validate", json={"csv": csv, "contract": contract}).status_code == 400
    )
