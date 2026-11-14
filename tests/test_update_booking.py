import pytest


def test_patch_booking_price(
        booking_client, created_booking, booking_data, auth_token
):
    booking_id = created_booking["bookingid"]
    changes = {"totalprice": 275}
    expected_booking = booking_data | changes

    response = booking_client.patch_booking(booking_id, changes, auth_token)

    assert response.status_code == 200
    assert response.json() == expected_booking

    saved = booking_client.get_booking(booking_id)
    assert saved.status_code == 200
    assert saved.json() == expected_booking


def test_put_booking_replaces_data(
        booking_client, created_booking, booking_data, auth_token
):
    booking_id = created_booking["bookingid"]
    replacement = booking_data | {
        "lastname": "Updated",
        "totalprice": 350,
        "depositpaid": False,
        "additionalneeds": "Dinner",
    }

    response = booking_client.put_booking(booking_id, replacement, auth_token)

    assert response.status_code == 200
    assert response.json() == replacement

    saved = booking_client.get_booking(booking_id)
    assert saved.status_code == 200
    assert saved.json() == replacement


@pytest.mark.parametrize(
    "token",
    [None, "invalid-token"],
    ids=["without-token", "invalid-token"],
)
def test_patch_booking_rejects_unauthorized_request(
        booking_client, created_booking, booking_data, token
):
    booking_id = created_booking["bookingid"]

    response = booking_client.patch_booking(
        booking_id, {"totalprice": 999}, token
    )

    assert response.status_code == 403

    saved = booking_client.get_booking(booking_id)
    assert saved.status_code == 200
    assert saved.json() == booking_data
