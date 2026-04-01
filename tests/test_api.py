import allure
import pytest

pytestmark = pytest.mark.api


@allure.feature("API. Корзина")
@allure.story("Добавление товара")
@allure.title("Добавление товара в корзину")
@allure.severity("critical")
def test_add_to_cart(api_client):
    barcode = "4610517829009"
    response = api_client.add_to_cart(barcode)

    items = response.get("items", [])
    assert len(items) > 0

    added_item = None
    for item in items:
        if item.get("offer", {}).get("barcode") == barcode:
            added_item = item

    assert added_item is not None
    assert added_item.get("quantity") == 1


@allure.feature("API. Корзина")
@allure.story("Изменение количества")
@allure.title("Изменение количества товара в корзине")
@allure.severity("critical")
def test_update_cart_item(api_client):
    barcode = "4610517829009"
    api_client.add_to_cart(barcode, 1)
    response = api_client.update_cart_item(barcode, 3)

    items = response.get("items", [])
    assert len(items) > 0

    updated_item = None
    for item in items:
        if item.get("offer", {}).get("barcode") == barcode:
            updated_item = item

    assert updated_item is not None
    assert updated_item.get("quantity") == 3


@allure.feature("API. Корзина")
@allure.story("Удаление товара")
@allure.title("Удаление товара из корзины")
@allure.severity("critical")
def test_remove_from_cart(api_client):
    barcode = "4610517829009"
    api_client.add_to_cart(barcode, 1)
    cart_before = api_client.get_cart()
    count_before = cart_before.get("total_count", 0)

    response = api_client.remove_from_cart(barcode)

    count_after = response.get("total_count", 0)
    assert count_after == count_before - 1


@allure.feature("API. Корзина")
@allure.story("Получение данных")
@allure.title("Получение содержимого корзины")
@allure.severity("high")
def test_get_cart(cart_with_item):
    response = cart_with_item.get_cart()

    assert "items" in response
    assert "total_count" in response
    assert "total_sum" in response


@allure.feature("API. Корзина")
@allure.story("Негативные сценарии")
@allure.title("Добавление товара с невалидным штрихкодом")
@allure.severity("high")
def test_negative_add_to_cart_invalid(api_client):
    invalid_barcode = "ABC0000000000000ABC"
    response = api_client.add_to_cart(invalid_barcode)

    assert "message" in response


@allure.feature("API. Избранное")
@allure.story("Добавление в избранное")
@allure.title("Добавление товара в избранное")
@allure.severity("normal")
def test_add_to_favorites(api_client):
    item_id = "ZR2604061308-99"
    api_client.add_to_favorites(item_id)

    user_info, status_code = api_client.get_user_info()
    assert status_code == 200
    favorites = user_info.get("favorites", [])

    assert item_id in favorites


@allure.feature("API. Доставка")
@allure.story("Получение способов доставки")
@allure.title("Получение способов доставки")
@allure.severity("high")
def test_get_shipping_methods(cart_with_item):

    address_kladr = "c2deb16a-0330-4f05-821f-1d09c93331e6"
    response, status_code = cart_with_item.get_shipping_methods(address_kladr)

    assert status_code == 200

    if len(response) > 0:
        assert "type" in response[0]
        assert "name" in response[0]


@allure.feature("API. Доставка")
@allure.story("Получение списка магазинов")
@allure.title("Получение списка магазинов")
@allure.severity("normal")
def test_get_shops(cart_with_item):

    city_kladr_id = "c2deb16a-0330-4f05-821f-1d09c93331e6"
    response, status_code = cart_with_item.get_shops(city_kladr_id)

    assert status_code == 200
    assert len(response) > 0


@allure.feature("API. Доставка")
@allure.story("Выбор магазина")
@allure.title("Выбор магазина для самовывоза")
@allure.severity("high")
def test_select_store(cart_with_item):

    store_id = "945"
    city_kladr_id = "c2deb16a-0330-4f05-821f-1d09c93331e6"
    response = cart_with_item.select_store(store_id, city_kladr_id)

    assert "basket" in response
    assert "shippings" in response
    assert response.get("cart_type") == "retail"
    assert response.get("shipping-method") == "retail"


@allure.feature("API. Оплата")
@allure.story("Получение способов оплаты")
@allure.title("Получение способов оплаты")
@allure.severity("high")
def test_get_payment_methods(cart_with_item):
    shipping_method = "retail"
    order_price = 12994
    shop = 945
    response = cart_with_item.get_payment_methods(
        shipping_method,
        order_price,
        shop
        )

    assert len(response) > 0
    assert "title" in response[0]
    assert "code" in response[0]


@allure.feature("API. Профиль")
@allure.story("Получение данных пользователя")
@allure.title("Получение персональных данных пользователя")
@allure.severity("normal")
def test_get_user_info(api_client):
    response, status_code = api_client.get_user_info()

    assert status_code == 200
    assert response is not None


@allure.feature("API. Профиль")
@allure.story("Негативные сценарии")
@allure.title("Изменение имени без авторизации")
@allure.severity("high")
def test_negative_update_profile_unauthorized(api_client_unauthorized):
    status_code = api_client_unauthorized.update_profile("Test", None)

    assert status_code == 403 or status_code == 401


@allure.feature("API. Промокоды")
@allure.story("Негативные сценарии")
@allure.title("Применение несуществующего промокода")
@allure.severity("high")
def test_negative_apply_invalid_promocode(cart_with_item):
    status_code = (
        cart_with_item.apply_promocode("Такого промокода не существует")
        )

    assert status_code != 200


# ========== ТЕСТЫ СЦЕНАРИЕВ ==========

@allure.feature("API. Сценарии")
@allure.story("Полный сценарий корзины")
@allure.title("Сценарий корзины: добавить товар, изменить количество, удалить")
@allure.severity("critical")
def test_full_cart_flow(api_client):
    barcode = "4610517829009"
    add_response = api_client.add_to_cart(barcode, 1)
    assert add_response.get("total_count", 0) > 0

    update_response = api_client.update_cart_item(barcode, 3)
    items = update_response.get("items", [])
    updated_item = None
    for item in items:
        if item.get("offer", {}).get("barcode") == barcode:
            updated_item = item
    assert updated_item is not None
    assert updated_item.get("quantity") == 3

    cart_response = api_client.get_cart()
    assert cart_response.get("total_count", 0) > 0

    remove_response = api_client.remove_from_cart(barcode)
    items = remove_response.get("items", [])
    found = False
    for item in items:
        if item.get("offer", {}).get("barcode") == barcode:
            found = True
    assert not found


@allure.feature("API. Сценарии")
@allure.story("Сценарий оформления заказа")
@allure.title("Сценарий оформления заказа: товар -> доставка -> оплата")
@allure.severity("high")
def test_checkout_flow(api_client):
    barcode = "4610517829009"
    city_kladr_id = "c2deb16a-0330-4f05-821f-1d09c93331e6"

    api_client.add_to_cart(barcode, 1)

    shipping_methods = api_client.get_shipping_methods(city_kladr_id)
    assert len(shipping_methods) > 0

    store_id = "945"
    api_client.select_store(store_id, city_kladr_id)

    cart = api_client.get_cart()
    order_price = cart.get("total_sum", 0)
    payment_methods = api_client.get_payment_methods(
        "retail", order_price, int(store_id))
    assert len(payment_methods) > 0
