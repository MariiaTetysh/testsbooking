import requests
from constants import BASE_URL, INVALID_BOOKING_ID, HEADERS, BOOKING_ENDPOINT


class TestBookings:

    def get_booking(self, requester, booking_id, booking_data=None, status_code=200):
        response = requester.send_request(
            method='GET',
            endpoint=f'{BOOKING_ENDPOINT}/{booking_id}',
            expected_status=status_code
        )
        if response.status_code == 200:
            response_data = response.json()

            assert response_data['firstname'] == booking_data['firstname'], (
                'Заданное имя не совпадает'
            )
            assert response_data['lastname'] == booking_data['lastname'], (
                'Заданное имя не совпадает'
            )
            assert response_data['totalprice'] == booking_data['totalprice'], (
                'Заданное имя не совпадает'
            )
            return response_data, booking_id

    def create_booking(self, requester, booking_data, status_code=200):
        response = requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=status_code
        )
        if response.status_code == 200:
            response_data = response.json()
            booking_id = response_data.get("bookingid")
            return response_data, booking_id

    def test_create_booking(
        self, requester, booking_data
    ):
        response_data, booking_id = self.create_booking(
            requester, booking_data
        )
        assert booking_id is not None, 'Идентификатор брони не найден в ответе'
        assert response_data['booking']['firstname'] == booking_data['firstname'], (
            'Заданное имя не совпадает'
        )
        assert response_data['booking']['totalprice'] == booking_data['totalprice'], (
            'Заданная стоимость не совпадает'
        )
        response = requester.send_request(
            method='GET',
            endpoint=f'{BOOKING_ENDPOINT}/{booking_id}',
            expected_status=200
        )
        response_data = response.json()
        assert response_data['lastname'] == booking_data['lastname'], (
            'Заданная фамилия не совпадает'
        )

    def test_delete_booking(
        self, requester, booking_data
    ):
        response = requester.send_request(
            method='POST',
            endpoint=BOOKING_ENDPOINT,
            data=booking_data,
            expected_status=200
        )
        response_data = response.json()
        booking_id = response_data.get("bookingid")

        response = requester.send_request(
            method='DELETE',
            endpoint=f'{BOOKING_ENDPOINT}/{booking_id}',
            expected_status=201
        )

        response = requester.send_request(
            method='GET',
            endpoint=f'{BOOKING_ENDPOINT}/{booking_id}',
            expected_status=404
        )

    def test_update_booking(
        self, requester, booking_data, new_booking_data
    ):
        response_data, booking_id = self.create_booking(
            requester, booking_data
        )
        response = requester.send_request(
            method='PUT',
            endpoint=f'{BOOKING_ENDPOINT}/{booking_id}',
            data=new_booking_data,
            expected_status=200
        )
        response = self.get_booking(requester, booking_id, new_booking_data)

    def test_partial_update(self, requester, booking_data):
        response_data, booking_id = self.create_booking(
            requester, booking_data
        )
        response = requester.send_request(
            method='PATCH',
            endpoint=f'{BOOKING_ENDPOINT}/{booking_id}',
            data={'firstname': 'Mariia'},
            expected_status=200
        )
        response = requester.send_request(
            method='GET',
            endpoint=f'{BOOKING_ENDPOINT}/{booking_id}',
            expected_status=200
        )
        assert response.json()['firstname'] == 'Mariia', (
            'Заданное имя не обновилось'
        )
        assert response.json()['lastname'] == booking_data['lastname'], (
            'Заданная фамилия обновилась без запроса'
        )

    def test_create_booking_with_invalid_data(
            self, requester, invalid_booking_data
    ):
        self.create_booking(requester, invalid_booking_data, status_code=500)

    def test_create_booking_with_not_all_data(self, requester):
        self.create_booking(requester, {'lastname': 'Hodge'}, status_code=500)

    def test_get_booking_with_invalid_booking_id(self, requester):
        self.get_booking(requester, INVALID_BOOKING_ID, status_code=404)

    def test_update_booking_with_invalid_booking_id(
        self, requester, booking_data
    ):
        response = requester.send_request(
            method='PUT',
            endpoint=f'{BOOKING_ENDPOINT}/{INVALID_BOOKING_ID}',
            data=booking_data,
            expected_status=405
        )

    def test_update_booking_with_empty_data(
        self, requester, booking_data,
        invalid_booking_data_with_no_data
    ):
        response_data, booking_id = self.create_booking(
            requester, booking_data
        )
        response = requester.send_request(
            method='PUT',
            endpoint=f'{BOOKING_ENDPOINT}/{booking_id}',
            data=invalid_booking_data_with_no_data,
            expected_status=400
        )
        self.get_booking(requester, booking_id, booking_data)

    def test_delete_booking_without_auth(self, requester, booking_data):
        create_booking = requests.post(
            f'{BASE_URL}{BOOKING_ENDPOINT}',
            headers=HEADERS,
            json=booking_data
        )
        booking_id = create_booking.json().get('bookingid')
        delete_booking = requests.delete(
            f'{BASE_URL}{BOOKING_ENDPOINT}/{booking_id}'
        )
        assert delete_booking.status_code == 403, (
            'Ошибка: бронирование удалено без необходимых прав доступа'
        )
        self.get_booking(requester, booking_id, booking_data)
