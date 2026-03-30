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
    """Фикстура для браузера (session scope)"""
    browser = webdriver.Chrome()
    browser.implicitly_wait(4)
    browser.maximize_window()
    yield browser

    browser.quit()


@pytest.fixture(scope="session")
def auth_cookies(browser, data_provider):
    """Фикстура для получения cookies после авторизации"""
    main_page = MainPage(browser)
    main_page.open()

    # Пытаемся загрузить существующие cookies
    if not main_page.auth_with_cookies():
        # Если нет — авторизуемся заново
        email = data_provider.get_email()
        password = data_provider.get_password()
        main_page.auth_with_email(email, password)

    return main_page
