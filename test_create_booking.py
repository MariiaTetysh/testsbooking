from constants import BASE_URL


class TestBookings:

    def test_create_booking(
        self, auth_session, booking_data, new_booking_data
    ):
        # Создаём бронирование
        create_booking = auth_session.post(
            f'{BASE_URL}/booking', json=booking_data
        )
        assert create_booking.status_code == 200, (
            'Ошибка создания бронирования'
        )

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, 'Идентификатор брони не найден в ответе'
        assert create_booking.json(

        )['booking']['firstname'] == booking_data['firstname'], (
            'Заданное имя не совпадает'
        )
        assert create_booking.json(

        )['booking']['totalprice'] == booking_data['totalprice'], (
            'Заданная стоимость не совпадает'
        )

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(
            f'{BASE_URL}/booking/{booking_id}'
        )
        assert get_booking.status_code == 200, (
            'Ошибка получения бронирования по id'
        )
        assert get_booking.json()['lastname'] == booking_data['lastname'], (
            'Заданная фамилия не совпадает'
        )

        # Удаляем бронирование
        deleted_booking = auth_session.delete(
            f'{BASE_URL}/booking/{booking_id}'
        )
        assert deleted_booking.status_code == 201, (
            'Ошибка удаления бронирования'
        )

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, 'Бронирование не удалилось'
