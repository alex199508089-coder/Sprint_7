import requests
import random
import string

from utils.constants import BASE_URL, COURIER_ENDPOINT


def register_new_courier_and_return_login_password():
    """
    Регистрирует нового курьера и возвращает список [login, password, firstName].
    Если регистрация не удалась, возвращает пустой список.
    """
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

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