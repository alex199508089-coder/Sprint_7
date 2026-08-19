def get_order_payload(color=None):
    """Возвращает тело запроса для создания заказа."""
    payload = {
        "firstName": "Alex",
        "lastName": "Ivanov",
        "address": "pr. Mira, 55",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-12-31",
        "comment": "Ostavit u dveri"
    }
    if color is not None:
        payload["color"] = color
    return payload