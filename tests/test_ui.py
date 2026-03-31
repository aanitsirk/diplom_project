import allure
from pages.MainPage import MainPage
from pages.CatalogPage import CatalogPage


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия модального окна авторизации")
@allure.severity("blocker")
def test_auth_modal_opens(browser_without_modals):
    main_page = MainPage(browser_without_modals)
    main_page.open()
    main_page.click_user_icon()
    assert main_page.auth_modal_is_visible()


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия модального окна корзины")
@allure.severity("critical")
def test_cart_modal_opens(browser_without_modals):
    main_page = MainPage(browser_without_modals)
    main_page.open()
    main_page.click_cart_icon()
    assert main_page.cart_modal_is_visible()


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия модального окна меню")
@allure.severity("critical")
def test_menu_modal_opens(browser_without_modals):
    main_page = MainPage(browser_without_modals)
    main_page.open()
    main_page.click_menu_burger()
    assert main_page.menu_modal_is_visible()


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка поиска товаров")
@allure.severity("high")
def test_search_items(browser_without_modals):
    main_page = MainPage(browser_without_modals)
    main_page.open()
    main_page.enter_search("Куртка")
    assert main_page.search_items_are_displayed()


@allure.feature("Главная страница")
@allure.story("UI тесты")
@allure.title("Проверка открытия каталога мужских товаров")
@allure.severity("critical")
def test_men_category_opens(browser_without_modals):
    main_page = MainPage(browser_without_modals)
    main_page.open()
    main_page.click_men_category()
    assert main_page.men_category_page()


@allure.feature("Каталог")
@allure.title("Проверка открытия карточки товара")
@allure.severity("high")
def test_open_item_card(browser_without_modals):
    catalog = CatalogPage(browser_without_modals)
    catalog.open_catalog()
    catalog.open_item_card()
    assert catalog.item_page_is_opened()


@allure.feature("Каталог")
@allure.title("Проверка добавления товара в корзину из каталога")
@allure.severity("critical")
def test_add_first_item_to_cart_from_catalog(browser_without_modals):
    from pages.MainPage import MainPage

    catalog = CatalogPage(browser_without_modals)
    catalog.open_catalog()
    item_name = catalog.add_first_item_to_cart_from_catalog()

    main_page = MainPage(browser_without_modals)
    main_page.click_cart_icon()

    assert main_page.cart_modal_is_visible()
    cart_item_name = catalog.item_is_in_cart(item_name)
    assert cart_item_name.lower() == item_name.lower()
