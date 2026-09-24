def test_profile_and_input_errors(client):
    assert client.post("/api/v1/profile", json={"csv": "a\n1\n2"}).json()["row_count"] == 2
    assert client.post("/api/v1/profile", json={"csv": "a,b\n1"}).status_code == 400
    assert (
        client.post("/api/v1/profile", json={"csv": "a", "path": "/etc/passwd"}).status_code == 422
    )
