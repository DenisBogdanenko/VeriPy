import pytest
from copy import deepcopy


def test_create_booking(created_booking, booking_data):
    assert created_booking["booking"] == booking_data


@pytest.mark.parametrize(
    "missing_field",
    [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
    ],
)
def test_create_booking_without_required_field_returns_server_error(
        booking_client, booking_data, missing_field
):
    incomplete_booking = booking_data.copy()
    incomplete_booking.pop(missing_field)

    response = booking_client.create_booking(incomplete_booking)

    assert response.status_code == 500
    assert response.text == "Internal Server Error"


@pytest.mark.parametrize("missing_date", ["checkin", "checkout"])
def test_create_booking_without_required_date_returns_server_error(
        booking_client, booking_data, missing_date
):
    incomplete_booking = deepcopy(booking_data)
    incomplete_booking["bookingdates"].pop(missing_date)

    response = booking_client.create_booking(incomplete_booking)

    assert response.status_code == 500
    assert response.text == "Internal Server Error"
