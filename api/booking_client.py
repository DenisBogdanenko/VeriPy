import requests


class BookingClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def ping(self) -> requests.Response:
        return requests.get(f"{self.base_url}/ping", timeout=10)

    def authenticate(self, username: str, password: str) -> requests.Response:
        return requests.post(
            f"{self.base_url}/auth",
            json={"username": username, "password": password},
            timeout=10,
        )

    def get_booking_ids(self, filters: dict | None = None) -> requests.Response:
        return requests.get(
            f"{self.base_url}/booking",
            params=filters,
            headers={"Accept": "application/json"},
            timeout=10,
        )

    def create_booking(self, booking: dict) -> requests.Response:
        return requests.post(
            f"{self.base_url}/booking",
            json=booking,
            headers={"Accept": "application/json"},
            timeout=10,
        )

    def delete_booking(
            self, booking_id: int, token: str | None = None
    ) -> requests.Response:
        return requests.delete(
            f"{self.base_url}/booking/{booking_id}",
            cookies={"token": token} if token is not None else None,
            timeout=10,
        )

    def get_booking(self, booking_id: int) -> requests.Response:
        return requests.get(
            f"{self.base_url}/booking/{booking_id}",
            headers={"Accept": "application/json"},
            timeout=10,
        )

    def patch_booking(
            self, booking_id: int, changes: dict, token: str | None = None
    ) -> requests.Response:
        return requests.patch(
            f"{self.base_url}/booking/{booking_id}",
            json=changes,
            cookies={"token": token} if token is not None else None,
            headers={"Accept": "application/json"},
            timeout=10,
        )

    def put_booking(
            self, booking_id: int, booking: dict, token: str | None = None
    ) -> requests.Response:
        return requests.put(
            f"{self.base_url}/booking/{booking_id}",
            json=booking,
            cookies={"token": token} if token is not None else None,
            headers={"Accept": "application/json"},
            timeout=10,
        )
