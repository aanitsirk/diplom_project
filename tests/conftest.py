import pytest
from selenium import webdriver
from pages.MainPage import MainPage
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
    main_page.close_all_modals()
    return browser


@pytest.fixture(scope="session")
def auth_cookies(browser, data_provider):
    """Фикстура для авторизованной сессии"""
    main_page = MainPage(browser)
    main_page.open()
    main_page.accept_city_modal()

    # Пытаемся загрузить существующие cookies
    if not main_page.auth_with_cookies():
        # Если нет — авторизуемся заново
        email = data_provider.get_email()
        password = data_provider.get_password()
        main_page.auth_with_email(email, password)

    return main_page
