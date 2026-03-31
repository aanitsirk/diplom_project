import allure
import pickle
import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


class MainPage:

    user_button = 'button:has(img[alt="User"])'
    auth_with_email_button = (
        'button.bg-white.text-main-black.border-light-grey'
    )
    cart_button = 'button:has(img[alt="Cart"])'
    menu_button = 'button:has(span[class*="relative"])'
    auth_button = '//button[.//span[text()="Войти"]]'
    accept_city_modal_button = '//button[contains(text(), "верно")]'
    clothes_button = '//button[contains(text(), "Одежда")]'
    view_all_button = '//a[contains(@href, "/catalog/clothes/") and contains(text(), "Смотреть все")]'

    email_input = '#Email'
    password_input = '#password'
    search_input = '[data-dgn-id="header-search-input"]'

    auth_modal = '.auth-content'
    cart_modal = '//h2[text()="Корзина"]'
    menu_modal = 'div[role="dialog"]:has(nav a[href="/man/"])'

    search_results = '.digi-products'
    men_category = 'a[href="/man/"]'

    def __init__(self, driver: WebDriver) -> None:
        self.__url = 'https://zarina.ru'
        self.__driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.__cookies_file = 'cookies.pkl'

    def wait_for_element(self, selector: str) -> None:
        """Ожидает появления элемента на странице"""
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, selector))
            )

    @allure.step("Открыть главную страницу")
    def open(self) -> None:
        """Открывает главную страницу"""
        self.__driver.get(self.__url)
        self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div")))

    @allure.step("Нажать на иконку 'Личный кабинет'")
    def click_user_icon(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, self.user_button).click()

    @allure.step("Проверить, что открыто модальное окно авторизации")
    def auth_modal_is_visible(self) -> bool:
        self.wait_for_element(self.auth_modal)
        return True

    @allure.step("Выполнить поисковый запрос: {item}")
    def enter_search(self, item: str) -> None:
        search_input = self.__driver.find_element(
            By.CSS_SELECTOR, self.search_input
            )
        search_input.clear()
        search_input.send_keys(item, Keys.RETURN)

    @allure.step("Проверить, что отображаются результаты поиска")
    def search_items_are_displayed(self) -> bool:
        self.wait_for_element(self.search_results)
        return True

    @allure.step("Нажать на кнопку 'Мужчинам'")
    def click_men_category(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, self.men_category).click()

    @allure.step("Проверить, что открыта страница мужских товаров")
    def men_category_page(self) -> bool:
        self.wait.until(EC.url_contains("/man/"))
        return True

    @allure.step("Нажать на иконку корзины")
    def click_cart_icon(self) -> None:
        cart_btn = self.__driver.find_element(By.CSS_SELECTOR, self.cart_button)
        self.__driver.execute_script("arguments[0].scrollIntoView(true);", cart_btn)
        self.__driver.execute_script("arguments[0].click();", cart_btn)

    @allure.step("Проверить, что открыто модальное окно корзины")
    def cart_modal_is_visible(self) -> bool:
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, self.cart_modal)))
        return True

    @allure.step("Нажать на кнопку выпадающего меню")
    def click_menu_burger(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, self.menu_button).click()

    @allure.step("Проверить, что открыто модальное окно меню")
    def menu_modal_is_visible(self) -> bool:
        self.wait_for_element(self.menu_modal)
        return True

    @allure.step("Открыть каталог женской одежды")
    def go_to_women_catalog(self) -> None:
        """Открывает каталог женской одежды через меню"""
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.clothes_button))).click()

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, self.view_all_button))).click()

    @allure.step("Авторизация через email: {email}")
    def auth_with_email(self, email: str, password: str) -> None:
        """Выполняет авторизацию и сохраняет cookies"""

        self.__driver.find_element(By.CSS_SELECTOR, self.user_button).click()
        self.wait_for_element(self.auth_with_email_button)
        self.__driver.find_element(
            By.CSS_SELECTOR, self.auth_with_email_button).click()
        self.wait_for_element(self.email_input)
        self.__driver.find_element(
            By.CSS_SELECTOR, self.email_input).send_keys(email)
        self.__driver.find_element(
            By.CSS_SELECTOR, self.password_input).send_keys(password)
        self.__driver.find_element(By.XPATH, self.auth_button).click()

        with open(self.__cookies_file, "wb") as f:
            pickle.dump(self.__driver.get_cookies(), f)

    @allure.step("Принять cookies")
    def accept_cookies(self) -> None:
        """Принимает cookies через добавление cookie в браузер"""
        cookie_policy = {
            'name': 'consent',
            'value': 'true'
        }

        cookies = self.__driver.get_cookies()
        current_cookies = [c for c in cookies if c.get('name') == 'consent']
        if not current_cookies:
            self.__driver.add_cookie(cookie_policy)

    @allure.step("Принять выбор города и закрыть модальное окно")
    def accept_city_modal(self) -> None:
        """Подтверждает выбор города"""
        self.__driver.find_elements(By.XPATH, self.accept_city_modal_button)
