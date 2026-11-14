from datetime import date, timedelta
from uuid import uuid4

from faker import Faker


fake = Faker("en_US")


def generate_booking_data() -> dict:
    checkin = date.today() + timedelta(days=7)

    return {
        "firstname": f"VeriPy-{fake.first_name()}-{uuid4().hex}",
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=200),
        "depositpaid": fake.pybool(),
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": (checkin + timedelta(days=2)).isoformat(),
        },
        "additionalneeds": fake.random_element(
            elements=("Breakfast", "Parking", "Late checkout"),
        ),
    }