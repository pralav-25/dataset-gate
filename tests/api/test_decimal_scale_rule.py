"""The decimal_scale rule is usable through the public validation endpoint."""


def test_decimal_scale_validation_and_catalog(client):
    contract = {
        "version": 1,
        "name": "decimal_scale integration",
        "rules": [
            {
                "id": "decimal-scale",
                "check": "decimal_scale",
                "params": {"places": 2},
                "column": "value",
            }
        ],
    }
    response = client.post(
        "/api/v1/validate", json={"csv": "value\n1.25\n1.251", "contract": contract}
    )
    assert response.status_code == 200
    finding = response.json()["results"][0]
    assert finding["check"] == "decimal_scale" and finding["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "decimal_scale" for rule in catalog)
    contract["rules"][0]["params"]["unknown"] = 1
    assert (
        client.post(
            "/api/v1/validate", json={"csv": "value\n1.25\n1.251", "contract": contract}
        ).status_code
        == 400
    )
