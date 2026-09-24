def test_rule_api(client):
    response = client.get("/api/v1/rules")
    assert response.status_code == 200 and len(response.json()) == 30
    assert any(row["name"] == "conditional_required" for row in response.json())
