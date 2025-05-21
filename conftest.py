import pytest
import requests
from faker import Faker
from constants import HEADERS, BASE_URL

faker = Faker()


@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f'{BASE_URL}/auth',
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )

    assert response.status_code == 200, 'Ошибка авторизации'
    token = response.json().get('token')
    assert token is not None, 'Ошибка: токен не существует'
    session.headers.update({'Cookie': f'token={token}'})
    return session


@pytest.fixture
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=1000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Piano"
    }


@pytest.fixture
def new_booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=1000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-05-05",
            "checkout": "2024-05-08"
        },
        "additionalneeds": "Breakfast"
    }


@pytest.fixture
def invalid_booking_data():
    return {
        "firstname": faker.random_int(min=3, max=25),
        "lastname": None,
        "totalprice": faker.date(),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }


@pytest.fixture
def invalid_booking_data_with_no_data():
    return {
        "firstname": None,
        "lastname": None,
        "totalprice": None,
        "depositpaid": None,
        "bookingdates": None,
        "additionalneeds": None
    }
