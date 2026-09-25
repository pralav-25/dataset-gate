"""The ip_address rule is usable through the public validation endpoint."""


def test_ip_address_validation_and_catalog(client):
    contract = {
        "version": 1,
        "name": "ip_address integration",
        "rules": [
            {
                "id": "ip-address",
                "check": "ip_address",
                "params": {"version": "any"},
                "column": "value",
            }
        ],
    }
    response = client.post(
        "/api/v1/validate", json={"csv": "value\n192.0.2.1\n999.1.2.3", "contract": contract}
    )
    assert response.status_code == 200
    finding = response.json()["results"][0]
    assert finding["check"] == "ip_address" and finding["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "ip_address" for rule in catalog)
    contract["rules"][0]["params"]["unknown"] = 1
    assert (
        client.post(
            "/api/v1/validate", json={"csv": "value\n192.0.2.1\n999.1.2.3", "contract": contract}
        ).status_code
        == 400
    )
