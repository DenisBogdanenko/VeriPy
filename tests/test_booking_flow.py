def test_booking_lifecycle(
    booking_client, created_booking, booking_data, auth_token
):
    booking_id = created_booking["bookingid"]
    assert created_booking["booking"] == booking_data

    # Читаем созданную запись.
    response = booking_client.get_booking(booking_id)

    assert response.status_code == 200
    assert response.json() == booking_data

    # Полностью обновляем бронирование.
    replacement = booking_data | {
        "lastname": "Updated",
        "totalprice": 350,
    }

    response = booking_client.put_booking(
        booking_id, replacement, auth_token
    )

    assert response.status_code == 200
    assert response.json() == replacement

    saved = booking_client.get_booking(booking_id)
    assert saved.status_code == 200
    assert saved.json() == replacement

    # Частично обновляем цену и состояние предоплаты.
    changes = {
        "totalprice": 275,
        "depositpaid": not replacement["depositpaid"],
    }
    expected_booking = replacement | changes

    response = booking_client.patch_booking(
        booking_id, changes, auth_token
    )

    assert response.status_code == 200
    assert response.json() == expected_booking

    saved = booking_client.get_booking(booking_id)
    assert saved.status_code == 200
    assert saved.json() == expected_booking

    # Удаляем запись и проверяем её отсутствие.
    response = booking_client.delete_booking(booking_id, auth_token)

    assert response.status_code == 201

    missing = booking_client.get_booking(booking_id)
    assert missing.status_code == 404