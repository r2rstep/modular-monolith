def test_create_rich_domain_resource(api_client):
    response = api_client.get("/crud")

    assert response.status_code == 200, response.json()
    assert "a" in response.json()
