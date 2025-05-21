from constants import BASE_URL


class TestUpdateBooking:

    def create_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(
            f'{BASE_URL}/booking',
            json=booking_data
        )
        booking_id = create_booking.json().get('bookingid')
        return booking_id

    def get_booking(self, auth_session, booking_id):
        get_booking = auth_session.get(
            f'{BASE_URL}/booking/{booking_id}'
        )
        return get_booking

    def test_update_booking(
        self, auth_session, booking_data, new_booking_data
    ):
        # Создаем бронирование
        booking_id = self.create_booking(auth_session, booking_data)
        # Обновляем полностью бронирование
        update_booking = auth_session.put(
            f'{BASE_URL}/booking/{booking_id}', json=new_booking_data
        )
        assert update_booking.status_code == 200, (
            'Ошибка обновления бронирования'
        )
        assert update_booking.json(

        )['firstname'] == new_booking_data['firstname'], (
            'Заданное имя не совпадает'
        )
        assert update_booking.json(

        )['lastname'] == new_booking_data['lastname'], (
            'Заданная фамилия не совпадает'
        )
        assert update_booking.json(

        )['totalprice'] == new_booking_data['totalprice'], (
            'Заданная стоимость не совпадает'
        )

        get_booking = self.get_booking(auth_session, booking_id)

        assert get_booking.status_code == 200, (
            'Ошибка: Бронирование не найдено'
        )
        assert get_booking.json(

        )['firstname'] == new_booking_data['firstname'], (
            'Заданное имя не совпадает'
        )
        assert get_booking.json(

        )['lastname'] == new_booking_data['lastname'], (
            'Заданная фамилия не совпадает'
        )
        assert get_booking.json(

        )['totalprice'] == new_booking_data['totalprice'], (
            'Заданная стоимость не совпадает'
        )

    def test_partial_update(self, auth_session, booking_data):
        # Создаем бронирование
        booking_id = self.create_booking(auth_session, booking_data)
        # Частично обновляем бронирование
        partial_update_booking = auth_session.patch(
            f'{BASE_URL}/booking/{booking_id}',
            json={'firstname': 'Mariia'}
        )
        assert partial_update_booking.status_code == 200
        assert partial_update_booking.json()['firstname'] == 'Mariia', (
            'Заданное имя не обновилось'
        )
        assert partial_update_booking.json(

        )['lastname'] == booking_data['lastname'], (
            'Заданная фамилия обновилась без запроса'
        )

        get_booking = self.get_booking(auth_session, booking_id)
        assert get_booking.status_code == 200, (
            'Ошибка: Бронирование не найдено'
        )
        assert get_booking.json()['firstname'] == 'Mariia', (
            'Заданное имя не обновилось'
        )
        assert get_booking.json()['lastname'] == booking_data['lastname'], (
            'Заданная фамилия обновилась без запроса'
        )
