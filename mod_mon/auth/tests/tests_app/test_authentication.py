def test_registration(api_client):
    response = api_client.post(
        "/registration",
        json={
            "email": "some@example.com",
            "password": "some_password",
        },
    )

    assert response.status_code == 200
