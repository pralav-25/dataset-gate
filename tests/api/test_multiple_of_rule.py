"""The multiple_of rule is usable through the public validation endpoint."""


def test_multiple_of_validation_and_catalog(client):
    contract = {
        "version": 1,
        "name": "multiple_of integration",
        "rules": [
            {
                "id": "multiple-of",
                "check": "multiple_of",
                "params": {"divisor": 0.05},
                "column": "value",
            }
        ],
    }
    response = client.post(
        "/api/v1/validate", json={"csv": "value\n0.15\n0.151", "contract": contract}
    )
    assert response.status_code == 200
    finding = response.json()["results"][0]
    assert finding["check"] == "multiple_of" and finding["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "multiple_of" for rule in catalog)
    contract["rules"][0]["params"]["unknown"] = 1
    assert (
        client.post(
            "/api/v1/validate", json={"csv": "value\n0.15\n0.151", "contract": contract}
        ).status_code
        == 400
    )
