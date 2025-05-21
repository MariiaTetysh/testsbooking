from constants import BASE_URL, INVALID_BOOKING_ID, HEADERS
import requests


class TestNegativeBooking:

    def get_booking(self, requests, booking_id, booking_data):
        get_booking = requests.get(
            f'{BASE_URL}/booking/{booking_id}'
        )
        assert get_booking.status_code == 200, (
            'Ошибка получения бронирования по id'
        )
        assert get_booking.json()['firstname'] == booking_data['firstname'], (
            'Заданное имя не совпадает'
        )
        assert get_booking.json()['lastname'] == booking_data['lastname'], (
            'Заданное имя не совпадает'
        )

    def test_create_booking_with_invalid_data(
        self, auth_session, invalid_booking_data
    ):
        create_booking = auth_session.post(
            f'{BASE_URL}/booking',
            json=invalid_booking_data
        )
        assert create_booking.status_code == 500, (
            'Ошибка: бронирование создано с невалидными данными'
        )

    def test_create_booking_with_not_all_data(self, auth_session):
        create_booking = auth_session.post(
            f'{BASE_URL}/booking',
            json={'lastname': 'Hodge'}
        )
        assert create_booking.status_code == 500, (
            'Ошибка: бронирование создано с невалидными данными'
        )

    def test_get_booking_with_invalid_booking_id(self, auth_session):
        get_booking = auth_session.get(
            f'{BASE_URL}/booking/{INVALID_BOOKING_ID}'
        )
        assert get_booking.status_code == 404, (
            'Ошибка: такого номера бронирования нет'
        )

    def test_update_booking_with_invalid_booking_id(
        self, auth_session, booking_data
    ):
        update_booking = auth_session.put(
            f'{BASE_URL}/booking/{INVALID_BOOKING_ID}',
            json=booking_data
        )
        assert update_booking.status_code == 405, (
            'Ошибка: такого номера бронирования нет, обновление невозможно'
        )

    def test_update_booking_with_empty_data(
        self, auth_session, booking_data,
        invalid_booking_data_with_no_data
    ):
        create_booking = auth_session.post(
            f'{BASE_URL}/booking',
            json=booking_data
        )
        booking_id = create_booking.json().get('bookingid')
        update_booking = auth_session.put(
            f'{BASE_URL}/booking/{booking_id}',
            json=invalid_booking_data_with_no_data
        )

        assert update_booking.status_code == 400, (
            'Ошибка обновления бронирования с пустыми данными'
        )
        self.get_booking(auth_session, booking_id, booking_data)

    def test_delete_booking_without_auth(self, booking_data):
        create_booking = requests.post(
            f'{BASE_URL}/booking',
            headers=HEADERS,
            json=booking_data
        )
        booking_id = create_booking.json().get('bookingid')
        delete_booking = requests.delete(
            f'{BASE_URL}/booking/{booking_id}'
        )
        assert delete_booking.status_code == 403, (
            'Ошибка: бронирование удалено без необходимых прав доступа'
        )
        self.get_booking(requests, booking_id, booking_data)
