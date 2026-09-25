"""The quantile_range rule is usable through the public validation endpoint."""


def test_quantile_range_validation_and_catalog(client):
    contract = {
        "version": 1,
        "name": "quantile_range integration",
        "rules": [
            {
                "id": "quantile-range",
                "check": "quantile_range",
                "params": {"q": 0.9, "min": 0, "max": 30},
                "column": "value",
            }
        ],
    }
    response = client.post("/api/v1/validate", json={"csv": "value\n40\n50", "contract": contract})
    assert response.status_code == 200
    finding = response.json()["results"][0]
    assert finding["check"] == "quantile_range" and finding["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "quantile_range" for rule in catalog)
    contract["rules"][0]["params"]["unknown"] = 1
    assert (
        client.post(
            "/api/v1/validate", json={"csv": "value\n40\n50", "contract": contract}
        ).status_code
        == 400
    )
