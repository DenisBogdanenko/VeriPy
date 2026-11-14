from jsonschema import FormatChecker, validate
from schemas.booking_schema import BOOKING_SCHEMA


def test_get_booking_ids(booking_client):
    response = booking_client.get_booking_ids()

    assert response.status_code == 200

    bookings = response.json()
    assert isinstance(bookings, list)

    for booking in bookings:
        assert type(booking["bookingid"]) is int


def test_get_booking_by_id(booking_client, created_booking, booking_data):
    response = booking_client.get_booking(created_booking["bookingid"])

    assert response.status_code == 200

    body = response.json()
    validate(
        instance=body,
        schema=BOOKING_SCHEMA,
        format_checker=FormatChecker(),
    )
    assert body == booking_data


def test_filter_booking_by_firstname(booking_client, created_booking):
    firstname = created_booking["booking"]["firstname"]

    response = booking_client.get_booking_ids(
        filters={"firstname": firstname}
    )

    assert response.status_code == 200
    assert response.json() == [
        {"bookingid": created_booking["bookingid"]}
    ]


def test_filter_booking_by_unknown_firstname(booking_client, created_booking):
    unknown_firstname = created_booking["booking"]["firstname"] + "-missing"

    response = booking_client.get_booking_ids(
        filters={"firstname": unknown_firstname}
    )

    assert response.status_code == 200
    assert response.json() == []
