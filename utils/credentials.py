import requests
import random
import string

from utils.constants import BASE_URL, COURIER_ENDPOINT

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_courier_credentials():
    """Генерирует случайные данные курьера без регистрации."""
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }


def register_new_courier_and_return_login_password():
    """
    Регистрирует нового курьера и возвращает список [login, password, firstName].
    Если регистрация не удалась, возвращает пустой список.
    """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }


    response = requests.post(f"{BASE_URL}{COURIER_ENDPOINT}", json=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    else:
        return []