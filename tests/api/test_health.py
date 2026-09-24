def test_health_and_openapi(client):
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/openapi.json").json()["info"]["title"] == "Dataset Gate"
