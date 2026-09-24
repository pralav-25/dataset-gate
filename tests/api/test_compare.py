def test_compare_api(client):
    response = client.post("/api/v1/compare", json={"before": "x\n1", "after": "x\n3"})
    assert response.status_code == 200 and response.json()["numeric"][0]["mean_delta"] == 2
