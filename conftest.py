import os

import pytest
from api.booking_client import BookingClient
from utils.data_generator import generate_booking_data


@pytest.fixture
def booking_client():
    base_url = os.getenv(
        "BOOKER_BASE_URL",
        "https://restful-booker.herokuapp.com",
    )
    return BookingClient(base_url)


@pytest.fixture
def booking_data():
    return generate_booking_data()


@pytest.fixture
def auth_token(booking_client):
    response = booking_client.authenticate("admin", "password123")
    assert response.status_code == 200

    token = response.json().get("token")
    assert isinstance(token, str) and token
    return token


@pytest.fixture
def created_booking(booking_client, booking_data, auth_token):
    response = booking_client.create_booking(booking_data)
    assert response.status_code == 200

    body = response.json()
    booking_id = body["bookingid"]
    assert type(booking_id) is int

    yield body

    current = booking_client.get_booking(booking_id)
    if current.status_code == 404:
        return

    assert current.status_code == 200

    deleted = booking_client.delete_booking(booking_id, auth_token)
    assert deleted.status_code == 201
