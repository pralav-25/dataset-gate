"""The string_case rule is usable through the public validation endpoint."""


def test_string_case_validation_and_catalog(client):
    contract = {
        "version": 1,
        "name": "string_case integration",
        "rules": [
            {
                "id": "string-case",
                "check": "string_case",
                "params": {"case": "lower"},
                "column": "value",
            }
        ],
    }
    response = client.post(
        "/api/v1/validate", json={"csv": "value\nhello\nHELLO", "contract": contract}
    )
    assert response.status_code == 200
    finding = response.json()["results"][0]
    assert finding["check"] == "string_case" and finding["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "string_case" for rule in catalog)
    contract["rules"][0]["params"]["unknown"] = 1
    assert (
        client.post(
            "/api/v1/validate", json={"csv": "value\nhello\nHELLO", "contract": contract}
        ).status_code
        == 400
    )
