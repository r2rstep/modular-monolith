def test_create_rich_domain_resource(api_client):
    response = api_client.post(
        "/rich_domain_resources",
        json={
            "name": "some_name",
        },
    )

    assert response.status_code == 200, response.json()
    assert "pk" in response.json()
