import allure
import pytest

from utils.constants import LOGIN_ENDPOINT


@allure.feature("Логин курьера")
class TestCourierLogin:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Курьер может авторизоваться, успешный запрос возвращает id")
    def test_login_courier_success(self, client, registered_courier):
        login_payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"]
        }
        response = client.post(LOGIN_ENDPOINT, json=login_payload)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}, тело: {response.text}"
        assert "id" in response.json(), "В ответе отсутствует поле id"

    @allure.title("Авторизация с неправильным логином или паролем")
    @allure.description("Система вернёт ошибку, если неправильно указать логин или пароль")
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_login_courier_wrong_credentials(self, client, registered_courier, wrong_field):
        login_payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"]
        }
        login_payload[wrong_field] = "wrong_" + login_payload[wrong_field]
        response = client.post(LOGIN_ENDPOINT, json=login_payload)
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}, тело: {response.text}"
        assert "Учетная запись не найдена" in response.text

    @allure.title("Авторизация с несуществующим пользователем")
    @allure.description("Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку")
    def test_login_courier_nonexistent_user(self, client):
        login_payload = {
            "login": "nonexistent_login_12345",
            "password": "nonexistent_password"
        }
        response = client.post(LOGIN_ENDPOINT, json=login_payload)
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}, тело: {response.text}"
        assert "Учетная запись не найдена" in response.text

    @allure.title("Авторизация без обязательного поля")
    @allure.description("Если какого-то поля нет, запрос возвращает ошибку  (код >= 400)")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field(self, client, registered_courier, missing_field):
        login_payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"]
        }
        login_payload.pop(missing_field)
        response = client.post(LOGIN_ENDPOINT, json=login_payload)
        assert response.status_code >= 400, f"Ожидался код ошибки (>=400), получен {response.status_code}, тело: {response.text}"