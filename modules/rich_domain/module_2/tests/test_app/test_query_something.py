def test_get_something(api_client):
    response = api_client.get("/some-endpoint", params={"param": "something"})

    assert response.status_code == 200, response.text
    assert response.json() == {"a": 1, "b": "something"}
