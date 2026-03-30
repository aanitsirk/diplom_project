import allure
from pages.MainPage import MainPage


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия модального окна авторизации")
@allure.severity("blocker")
def test_auth_modal_opens(browser):
    main_page = MainPage(browser)
    main_page.open()
    main_page.click_user_icon()
    assert main_page.auth_modal_is_visible()


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия модального окна корзины")
@allure.severity("critical")
def test_cart_modal_opens(browser):
    main_page = MainPage(browser)
    main_page.open()
    main_page.click_cart_icon()
    assert main_page.cart_modal_is_visible()


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия модального окна меню")
@allure.severity("critical")
def test_menu_modal_opens(browser):
    main_page = MainPage(browser)
    main_page.open()
    main_page.click_menu_burger()
    assert main_page.menu_modal_is_visible()


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка поиска товаров")
@allure.severity("high")
def test_search_items(browser):
    main_page = MainPage(browser)
    main_page.open()
    main_page.enter_search("Куртка")
    assert main_page.search_items_are_displayed()


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия каталога мужских товаров")
@allure.severity("critical")
def test_men_category_opens(browser):
    main_page = MainPage(browser)
    main_page.open()
    main_page.click_men_category()
    assert main_page.men_category_page()
