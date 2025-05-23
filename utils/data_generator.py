import random
import string
import datetime
from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )
        return f'kek{random_string}@gmail.com'

    @staticmethod
    def generate_random_first_name():
        return f'{faker.first_name()}'

    @staticmethod
    def generate_random_last_name():
        return f'{faker.last_name()}'

    @staticmethod
    def generate_random_totalprice():
        return faker.random_int(min=100, max=1000)

    @staticmethod
    def generate_random_depositpaid():
        return faker.boolean()

    @staticmethod
    def generate_random_bookingdates():
        start_date = datetime.date.today()
        checkin_date = start_date + datetime.timedelta(
            days=random.randint(0, 100)
        )
        stay_duration = random.randint(1, 14)
        checkout_date = checkin_date + datetime.timedelta(days=stay_duration)
        return {
            "checkin": checkin_date.strftime("%Y-%m-%d"),
            "checkout": checkout_date.strftime("%Y-%m-%d")
        }

    @staticmethod
    def generate_random_additionalneeds():
        additionalneeds = [
            'Breakfast', 'Сradle', 'Plate of fruit', 'Dog bed', None
        ]
        random_additionalneeds = random.choice(additionalneeds)
        return random_additionalneeds

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remainig_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remainig_chars)
        random.shuffle(password)

        return ''.join(password)
