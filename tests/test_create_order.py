import allure
import pytest

from utils.constants import ORDERS_ENDPOINT
from utils.order_data import get_order_payload


@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с различными вариантами цветов")
    @allure.description("Параметризованный тест: можно указать BLACK, GREY, оба цвета или не указывать цвет")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_with_colors(self, client, color):
        payload = get_order_payload(color=color)
        with allure.step("Создание заказа"):
            response = client.post(ORDERS_ENDPOINT, json=payload)
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}, тело: {response.text}"
        assert "track" in response.json(), "В ответе отсутствует поле track"