def test_ping(booking_client):
    response = booking_client.ping()

    assert response.status_code == 201