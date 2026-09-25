"""The nonblank_count rule is usable through the public validation endpoint."""


def test_nonblank_count_validation_and_catalog(client):
    contract = {
        "version": 1,
        "name": "nonblank_count integration",
        "rules": [
            {
                "id": "nonblank-count",
                "check": "nonblank_count",
                "params": {"columns": ["a", "b"], "min": 1, "max": 1},
            }
        ],
    }
    response = client.post("/api/v1/validate", json={"csv": "a,b\nx,\nx,y", "contract": contract})
    assert response.status_code == 200
    finding = response.json()["results"][0]
    assert finding["check"] == "nonblank_count" and finding["failed"] == 1
    catalog = client.get("/api/v1/rules").json()
    assert any(rule["name"] == "nonblank_count" for rule in catalog)
    contract["rules"][0]["params"]["unknown"] = 1
    assert (
        client.post(
            "/api/v1/validate", json={"csv": "a,b\nx,\nx,y", "contract": contract}
        ).status_code
        == 400
    )
