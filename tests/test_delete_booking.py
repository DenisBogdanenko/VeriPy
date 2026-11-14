import pytest


def test_delete_booking(booking_client, created_booking, auth_token):
    booking_id = created_booking["bookingid"]

    response = booking_client.delete_booking(booking_id, auth_token)

    assert response.status_code == 201

    missing_booking = booking_client.get_booking(booking_id)
    assert missing_booking.status_code == 404


@pytest.mark.parametrize(
    "token",
    [None, "invalid-token"],
    ids=["without-token", "invalid-token"],
)
def test_delete_booking_rejects_unauthorized_request(
        booking_client, created_booking, booking_data, token
):
    booking_id = created_booking["bookingid"]

    response = booking_client.delete_booking(booking_id, token)

    assert response.status_code == 403

    saved = booking_client.get_booking(booking_id)
    assert saved.status_code == 200
    assert saved.json() == booking_data


@pytest.mark.parametrize(
    "token",
    [None, "invalid-token"],
    ids=["without-token", "invalid-token"],
)
def test_put_booking_rejects_unauthorized_request(
    booking_client, created_booking, booking_data, token
):
    booking_id = created_booking["bookingid"]
    replacement = booking_data | {
        "lastname": "Unauthorized",
        "totalprice": 999,
    }

    response = booking_client.put_booking(booking_id, replacement, token)

    assert response.status_code == 403

    saved = booking_client.get_booking(booking_id)
    assert saved.status_code == 200
    assert saved.json() == booking_data