import allure

from utils.constants import ORDERS_ENDPOINT


@allure.feature("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    @allure.description("Проверяет, что в тело ответа возвращается список заказов")
    def test_get_orders_list(self, client):
        response = client.get(ORDERS_ENDPOINT)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}, тело: {response.text}"
        data = response.json()
        assert "orders" in data, "В ответе отсутствует ключ 'orders'"
        assert isinstance(data["orders"], list), "Поле 'orders' должно быть списком"
