import allure
import pytest

from utils.constants import COURIER_ENDPOINT, LOGIN_ENDPOINT


@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.title("Успешное создание курьера")
    @allure.description("Проверяет, что курьера можно создать, код ответа 201 и тело содержит ok: true")
    def test_create_courier_success(self, client, courier_data, delete_courier):
        with allure.step("Создание курьера"):
            response = client.post(COURIER_ENDPOINT, json=courier_data)
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}, тело: {response.text}"
        assert response.json().get("ok") is True, "Поле 'ok' отсутствует или не равно true"

        with allure.step("Логин для получения id курьера"):
            login_payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }
            login_response = client.post(LOGIN_ENDPOINT, json=login_payload)
            courier_id = login_response.json()["id"]

        delete_courier(courier_id)

    @allure.title("Создание курьера с уже существующим логином")
    @allure.description("Нельзя создать двух одинаковых курьеров, возвращается ошибка")
    def test_create_courier_duplicate_login(self, client, registered_courier):
        duplicate_payload = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
            "firstName": registered_courier["firstName"]
        }
        with allure.step("Попытка создания курьера с существующим логином"):
            response = client.post(COURIER_ENDPOINT, json=duplicate_payload)
        assert response.status_code in [400, 409], f"Ожидался код 400 или 409, получен {response.status_code}, тело: {response.text}"
        assert "message" in response.json(), "В ответе отсутствует поле message"
        assert response.json()["message"] != "", "Сообщение об ошибке пустое"

    @allure.title("Создание курьера без обязательного поля")
    @allure.description("Если одного из полей нет, запрос возвращает ошибку 400")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, client, courier_data, missing_field):
        payload = courier_data.copy()
        payload.pop(missing_field)
        with allure.step(f"Создание курьера без поля {missing_field}"):
            response = client.post(COURIER_ENDPOINT, json=payload)
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}, тело: {response.text}"
        assert "Недостаточно данных для создания учетной записи" in response.text