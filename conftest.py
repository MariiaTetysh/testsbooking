import pytest
import requests
from faker import Faker

from constants import HEADERS, BASE_URL, AUTH_ENDPOINT
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester

faker = Faker()

@pytest.fixture(scope='function')
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    return {
        "username": "admin",
        "password": "password123"
    }


@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=AUTH_ENDPOINT,
        data=test_user,
        expected_status=200
    )
    response_data = response.json()
    registered_user = test_user.copy()
    token = response_data.get('token')
    assert token is not None
    return registered_user


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    auth_response = requests.post(
        f'{BASE_URL}{AUTH_ENDPOINT}',
        json={"username": "admin", "password": "password123"}
    )
    token = auth_response.json().get('token')
    assert token is not None
    return CustomRequester(session=session, base_url=BASE_URL, token=token)


@pytest.fixture(scope='function')
def booking_data():
    random_first_name = DataGenerator.generate_random_first_name()
    random_last_name = DataGenerator.generate_random_last_name()
    random_totalprice = DataGenerator.generate_random_totalprice()
    random_depositpaid = DataGenerator.generate_random_depositpaid()
    random_bookingdates = DataGenerator.generate_random_bookingdates()
    random_additionalneeds = DataGenerator.generate_random_additionalneeds()

    return {
        "firstname": random_first_name,
        "lastname": random_last_name,
        "totalprice": random_totalprice,
        "depositpaid": random_depositpaid,
        "bookingdates": random_bookingdates,
        "additionalneeds": random_additionalneeds
    }


@pytest.fixture(scope='function')
def new_booking_data():
    random_first_name = DataGenerator.generate_random_first_name()
    random_last_name = DataGenerator.generate_random_last_name()
    random_totalprice = DataGenerator.generate_random_totalprice()
    random_depositpaid = DataGenerator.generate_random_depositpaid()
    random_bookingdates = DataGenerator.generate_random_bookingdates()
    random_additionalneeds = DataGenerator.generate_random_additionalneeds()

    return {
        "firstname": random_first_name,
        "lastname": random_last_name,
        "totalprice": random_totalprice,
        "depositpaid": random_depositpaid,
        "bookingdates": random_bookingdates,
        "additionalneeds": random_additionalneeds
    }


@pytest.fixture(scope='function')
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


@pytest.fixture(scope='function')
def invalid_booking_data_with_no_data():
    return {
        "firstname": None,
        "lastname": None,
        "totalprice": None,
        "depositpaid": None,
        "bookingdates": None,
        "additionalneeds": None
    }
