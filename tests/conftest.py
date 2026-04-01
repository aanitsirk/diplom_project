import pytest
from selenium import webdriver
from pages.MainPage import MainPage
from api.api_client import ZarinaApi
from testdata.data_provider import DataProvider


@pytest.fixture(scope="session")
def data_provider():
    """Фикстура для доступа к тестовым данным"""
    return DataProvider()


@pytest.fixture(scope="session")
def browser():
    """Фикстура для браузера"""
    browser = webdriver.Chrome()
    browser.implicitly_wait(4)
    browser.maximize_window()
    yield browser

    browser.quit()


@pytest.fixture
def browser_without_modals(browser):
    """Фикстура закрывает модальные окна (город и cookies)"""
    main_page = MainPage(browser)
    main_page.open()
    main_page.accept_city_modal()
    main_page.accept_cookies()
    return browser


@pytest.fixture(scope="session")
def auth_browser(browser, data_provider):
    """Фикстура для авторизованного браузера (один раз на сессию)"""
    main_page = MainPage(browser)
    main_page.open()
    main_page.accept_city_modal()

    email = data_provider.get_email()
    password = data_provider.get_password()
    main_page.auth_with_email(email, password)

    return browser


@pytest.fixture
def api_client(data_provider):
    """Фикстура для API-клиента с авторизацией через API"""
    client = ZarinaApi()
    email = data_provider.get_email()
    password = data_provider.get_password()

    client.auth_by_email(email, password)

    return client


@pytest.fixture
def api_client_unauthorized():
    """Фикстура для неавторизованного API-клиента"""
    return ZarinaApi()


@pytest.fixture
def cart_with_item(api_client):
    """Фикстура добавляет товар в корзину и возвращает клиент"""
    barcode = "4610517829009"
    api_client.add_to_cart(barcode, 1)
    return api_client
