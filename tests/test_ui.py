import allure
from pages.MainPage import MainPage


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия модального окна авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_auth_modal_opens(browser):
    main_page = MainPage(browser)
    main_page.open()
    main_page.click_user_icon()
    assert main_page.auth_modal_is_visible()


@allure.feature("Главная страница")
@allure.title("Открытие главной страницы")
def test_open(browser):
    main_page = MainPage(browser)
    main_page.open()
    assert browser.current_url == "https://zarina.ru/"


@allure.title("Авторизация через email")
def test_auth(auth_cookies):
    """Тест использует авторизованную сессию"""
    # auth_cookies уже содержит авторизованную сессию
    assert auth_cookies is not None