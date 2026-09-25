"""The median_range rule is usable through the public validation endpoint."""


def test_median_range_validation_and_catalog(client):
    contract = {
        "version": 1,
        "name": "median_range integration",
        "rules": [
            {
                "id": "median-range",
                "check": "median_range",
                "params": {"min": 2, "max": 4},
                "column": "value",
            }
        ],
    }
    response = client.post("/api/v1/validate", json={"csv": "value\n8\n10", "contract": contract})
    assert response.status_code == 200
    finding = response.json()["results"][0]
    assert finding["check"] == "median_range" and finding["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "median_range" for rule in catalog)
    contract["rules"][0]["params"]["unknown"] = 1
    assert (
        client.post(
            "/api/v1/validate", json={"csv": "value\n8\n10", "contract": contract}
        ).status_code
        == 400
    )
