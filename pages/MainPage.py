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
    email_input = '#Email'
    password_input = '#password'
    auth_button = '//button[.//span[text()="Войти"]]'

    auth_modal = '.auth-content'
    cart_modal = 'div[role="dialog"]'
    menu_modal = 'div[role="dialog"]:has(nav a[href="/man/"])'
    search_input = '[data-dgn-id="header-search-input"]'
    search_results = '.digi-products'
    men_category = 'a[href="/man/"]'
    cart_button = 'button:has(img[alt="Cart"])'
    menu_button = 'button:has(span[class*="relative"])'

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
        return self.__driver.current_url == "https://zarina.ru/man/"

    @allure.step("Нажать на иконку корзины")
    def click_cart_icon(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, self.cart_button).click()

    @allure.step("Проверить, что открыто модальное окно корзины")
    def cart_modal_is_visible(self) -> bool:
        self.wait_for_element(self.cart_modal)
        return True

    @allure.step("Нажать на кнопку меню (бургер)")
    def click_menu_burger(self) -> None:
        self.__driver.find_element(By.CSS_SELECTOR, self.menu_button).click()

    @allure.step("Проверить, что открыто модальное окно меню")
    def menu_modal_is_visible(self) -> bool:
        self.wait_for_element(self.menu_modal)
        return True

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

    @allure.step("Авторизация через сохраненные cookies")
    def auth_with_cookies(self) -> bool:
        """Загружает cookies и возвращает True, если авторизация успешна"""
        if os.path.exists(self.__cookies_file):
            with open(self.__cookies_file, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    self.__driver.add_cookie(cookie)
            self.__driver.refresh()
            return True
        else:
            return False
