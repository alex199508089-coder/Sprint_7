import pytest
import allure

from utils.api_client import ApiClient
from utils.credentials import generate_courier_credentials, register_new_courier_and_return_login_password
from utils.constants import BASE_URL, COURIER_ENDPOINT, LOGIN_ENDPOINT



@pytest.fixture(scope="session")
def client():
    return ApiClient(BASE_URL)


@pytest.fixture
def courier_data():
    """Генерирует данные курьера без регистрации."""
    return generate_courier_credentials()


@pytest.fixture
def delete_courier(client):
    """Фикстура, возвращающая функцию для удаления курьера по id."""
    def _delete_courier(courier_id):
        with allure.step(f"Удаление курьера с id={courier_id}"):
            return client.delete(f"{COURIER_ENDPOINT}/{courier_id}")
    return _delete_courier


@pytest.fixture
def registered_courier(client):
    """
    Создаёт курьера через функцию регистрации, выполняет логин для получения id,
    возвращает словарь с данными и id. После теста удаляет курьера.
    """
    courier_credentials = register_new_courier_and_return_login_password()
    if len(courier_credentials) != 3:
        raise RuntimeError("Не удалось зарегистрировать курьера")

    login, password, first_name = courier_credentials

    with allure.step("Логин курьера для получения id"):
        login_payload = {
            "login": login,
            "password": password
        }
        login_response = client.post(LOGIN_ENDPOINT, json=login_payload)
        courier_id = login_response.json()["id"]

    courier_info = {
        "login": login,
        "password": password,
        "firstName": first_name,
        "id": courier_id
    }

    yield courier_info

    with allure.step("Удаление курьера"):
        client.delete(f"{COURIER_ENDPOINT}/{courier_id}")