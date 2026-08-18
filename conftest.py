import pytest
import requests
import allure

from utils.constants import BASE_URL, COURIER_ENDPOINT, LOGIN_ENDPOINT
from utils.credentials import register_new_courier_and_return_login_password


class ApiClient:
    """
    Обёртка над requests.Session, автоматически добавляющая базовый URL
    ко всем запросам с относительными путями.
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def request(self, method, url, **kwargs):

        if not url.startswith("http"):
            url = self.base_url + url
        return self.session.request(method, url, **kwargs)

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)


@pytest.fixture(scope="session")
def client():
    """Фикстура для HTTP-клиента с базовым URL."""
    return ApiClient(BASE_URL)


@pytest.fixture
def courier_data():
    """
    Генерирует случайные данные курьера без предварительной регистрации.
    Используется в тестах создания курьера.
    """
    import random
    import string

    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }


@pytest.fixture
def registered_courier(client):
    """
    Создаёт курьера через функцию регистрации, выполняет логин для получения id,
    возвращает словарь с данными и id. После теста удаляет курьера.
    """
    courier_credentials = register_new_courier_and_return_login_password()
    assert len(courier_credentials) == 3, "Не удалось зарегистрировать курьера"

    login, password, first_name = courier_credentials


    login_payload = {
        "login": login,
        "password": password
    }
    login_response = client.post(LOGIN_ENDPOINT, json=login_payload)
    assert login_response.status_code == 200, f"Не удалось авторизоваться: {login_response.text}"
    courier_id = login_response.json()["id"]

    courier_info = {
        "login": login,
        "password": password,
        "firstName": first_name,
        "id": courier_id
    }

    yield courier_info


    with allure.step("Удаление курьера"):
        delete_response = client.delete(f"{COURIER_ENDPOINT}/{courier_id}")
        assert delete_response.status_code in [200, 404], f"Не удалось удалить курьера: {delete_response.text}"