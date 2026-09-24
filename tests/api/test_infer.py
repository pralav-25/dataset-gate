def test_inference(client):
    response = client.post("/api/v1/infer", json={"csv": "id\n001", "name": "Tickets"})
    assert response.status_code == 200
    assert response.json()["rules"][1]["params"]["type"] == "string"
