def test_get_something(api_client):
    param_val = "something"
    response = api_client.get("/some-endpoint", params={"param": param_val})

    assert response.status_code == 200, response.text
    assert response.json() == {"a": 1, "b": "1" + param_val}
