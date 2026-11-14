def test_auth_returns_token(booking_client):
    response = booking_client.authenticate("admin", "password123")

    assert response.status_code == 200

    token = response.json().get("token")
    assert isinstance(token, str)
    assert token


def test_auth_rejects_invalid_password(booking_client):
    response = booking_client.authenticate("admin", "wrong-password")

    assert response.status_code == 200

    body = response.json()
    assert body["reason"] == "Bad credentials"
    assert "token" not in body