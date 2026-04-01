import requests
import allure
from config.settings import settings


class ZarinaApi:

    base_url = settings.api_base_url

    def __init__(self) -> None:
        self.cookies = None
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def set_cookies(self, cookies: dict) -> None:
        """Устанавливает cookies для запросов"""
        self.cookies = cookies

    def get_headers(self) -> dict:
        return self.headers

    @allure.step("Авторизация по email")
    def auth_by_email(self,
                      email: str,
                      password: str,
                      captcha_token: str = "") -> dict:
        """Авторизуется по email и паролю"""
        url = f'{self.base_url}/auth/email'
        payload = {
            "email": email,
            "password": password,
            "smartCaptchaToken": captcha_token
        }
        response = requests.post(url, headers=self.get_headers(), json=payload)

        if response.cookies:
            self.cookies = response.cookies.get_dict()

        return response.json()

    @allure.step("Получить персональные данные пользователя")
    def get_user_info(self) -> tuple:
        """
        Возвращает информацию о пользователе
        (имя, фамилия, избранное, бонусы и т.д.)
        """
        url = f'{self.base_url}/auth/init/'
        response = requests.get(url,
                                headers=self.get_headers(),
                                cookies=self.cookies)

        return response.json(), response.status_code

    @allure.step("Добавить товар в корзину по штрихкоду")
    def add_to_cart(self, barcode: str, quantity: int = 1) -> dict:
        """Добавляет товар в корзину по штрихкоду"""
        url = f'{self.base_url}/cart/item/'
        payload = {
            "barcode": barcode,
            "quantity": quantity,
            "cart_type": "undefined"
        }
        response = requests.post(url,
                                 headers=self.get_headers(),
                                 cookies=self.cookies,
                                 json=payload)
        return response.json()

    @allure.step("Изменить количество товара в корзине")
    def update_cart_item(self, barcode: str, quantity: int) -> dict:
        """Изменяет количество товара в корзине по штрихкоду"""
        url = f'{self.base_url}/cart/item/update/'
        payload = {
            "barcode": barcode,
            "quantity": quantity,
            "cart_type": "undefined"
        }
        response = requests.post(url,
                                 headers=self.get_headers(),
                                 cookies=self.cookies,
                                 json=payload)
        return response.json()

    @allure.step("Удалить товар из корзины")
    def remove_from_cart(self, barcode: str) -> dict:
        """Удаляет товар из корзины по штрихкоду"""
        url = f'{self.base_url}/cart/item/remove/'
        payload = {
            "barcode": barcode,
            "cart_type": "undefined",
            "quantity": 0
        }
        response = requests.post(url,
                                 headers=self.get_headers(),
                                 cookies=self.cookies,
                                 json=payload)
        return response.json()

    @allure.step("Получить содержимое корзины")
    def get_cart(self,
                 cart_type: str = "undefined",
                 payment_method: str = "") -> dict:
        """Возвращает текущее содержимое корзины"""
        url = f'{self.base_url}/cart/'
        params = {
            "cart_type": cart_type,
            "payment_method": payment_method
        }
        response = requests.get(url,
                                headers=self.get_headers(),
                                cookies=self.cookies,
                                params=params)
        return response.json()

    @allure.step("Добавить товар в избранное")
    def add_to_favorites(self, item_id: str) -> dict:
        """Добавляет товар в избранное по ID товара"""
        url = f'{self.base_url}/favorites/product/{item_id}/add/'
        response = requests.get(url,
                                headers=self.get_headers(),
                                cookies=self.cookies)
        return response.json()

    @allure.step("Получить способы доставки")
    def get_shipping_methods(self,
                             address_kladr: str,
                             cart_type: str = "undefined") -> tuple:
        """Получает доступные способы доставки по адресу"""
        url = f'{self.base_url}/shipping-methods/'
        params = {
            "cart_type": cart_type,
            "address_kladr": address_kladr
        }
        response = requests.get(url,
                                headers=self.get_headers(),
                                cookies=self.cookies,
                                params=params)

        return response.json(), response.status_code

    @allure.step("Получить список магазинов для самовывоза")
    def get_shops(self, city_kladr_id: str, shipping: str = "retail") -> tuple:
        """Получает список магазинов для способа 'Забрать из магазина'"""
        url = f'{self.base_url}/shipping-methods/shops/'
        params = {
            "city_kladr_id": city_kladr_id,
            "shipping": shipping
        }
        response = requests.get(url,
                                headers=self.get_headers(),
                                cookies=self.cookies,
                                params=params)

        return response.json(), response.status_code

    @allure.step("Выбрать магазин для самовывоза")
    def select_store(self,
                     store_id: str,
                     city_kladr_id: str,
                     shipping_type: str = "retail") -> dict:
        """Выбирает магазин для способа доставки 'Забрать из магазина'"""
        url = f'{self.base_url}/cart/'
        params = {
            "cart_type": "retail",
            "payment_method": "",
            "store_id": store_id,
            "shipping[shipping_method_type]": shipping_type,
            "shipping[address][city_kladr_id]": city_kladr_id,
            "shipping[address][city_name]": "",
            "shipping[address][street_kladr_id]": "",
            "shipping[address][street_name]": "",
            "shipping[address][building_kladr_id]": "",
            "shipping[address][building_number]": "",
            "shipping[address][flat]": "",
            "shipping[address][zipcode]": "",
            "shipping[payload][shop_id]": store_id,
            "shipping[payload][city]": "Санкт-Петербург"
        }
        response = requests.get(url,
                                headers=self.get_headers(),
                                cookies=self.cookies,
                                params=params)
        return response.json()

    @allure.step("Получить список способов оплаты")
    def get_payment_methods(self,
                            shipping_method: str,
                            order_price: int,
                            shop: int = None) -> dict:
        """Получает доступные способы оплаты"""
        url = f'{self.base_url}/payment-methods/'
        params = {
            "shipping_method": shipping_method,
            "order_price": order_price
        }
        if shop:
            params["shop"] = shop
        response = requests.get(url,
                                headers=self.get_headers(),
                                cookies=self.cookies,
                                params=params)
        return response.json()

    @allure.step("Изменить данные пользователя")
    def update_profile(self, first_name: str, last_name: str = None) -> int:
        """Обновляет имя и фамилию пользователя"""
        url = f'{self.base_url}/v1/profile/'
        payload = {"first_name": first_name}
        if last_name:
            payload["last_name"] = last_name

        response = requests.put(url,
                                headers=self.get_headers(),
                                cookies=self.cookies,
                                json=payload)

        return response.status_code

    @allure.step("Добавить товар в корзину с невалидным ID")
    def add_to_cart_invalid(self, product_id: str) -> dict:
        url = f'{self.base_url}/cart/item/'
        payload = {"product_id": product_id, "quantity": 1}
        response = requests.post(url,
                                 headers=self.get_headers(),
                                 cookies=self.cookies,
                                 json=payload)
        return response.json()

    @allure.step("Применить несуществующий промокод")
    def apply_promocode(self, promocode: str) -> int:
        url = f'{self.base_url}/cart/promocode/'
        payload = {"promocode": promocode}
        response = requests.post(url,
                                 headers=self.get_headers(),
                                 cookies=self.cookies,
                                 json=payload)
        return response.status_code
