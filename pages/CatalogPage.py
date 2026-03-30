import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class CatalogPage:

    sort_dropdown = 'button[role="combobox"]'
    sort_option = 'div[role="option"]'
    sort_options = {
        "newest": "По новизне",
        "popular": "По популярности",
        "sale": "По скидке",
        "price_asc": "Цена по возрастанию",
        "price_desc": "Цена по убыванию"
    }

    item_cards = '.catalog-item'
    item_title = '.product-title'
    item_info = '.product-info'
    item_image = 'img[alt="image"]'

    first_item_title = '.product-title a'    
    cart_button = '.product-cart img[alt="Cart"]'
    size_modal = '.cursor-pointer:not(.text-middle-gray)'
    cart_modal = 'div[role="dialog"]'
    cart_item = '.cart-item'
    cart_item_title = '.cart-item h3'
    cart_item_size = '.cart-item .text-xxs.uppercase.text-main-black'

    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        self.__url = 'https://zarina.ru/catalog/'
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element(self, selector: str) -> None:
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, selector)))

    @allure.step("Открыть страницу каталога")
    def open_catalog(self) -> None:
        """Открывает страницу каталога"""
        self.__driver.get(self.__url)

    @allure.step("Открыть категорию: {category_name}")
    def open_category(self, category_name: str) -> None:
        """Открывает категорию товаров по названию"""
        category_xpath = f'//a[contains(text(), "{category_name}")]'
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, category_xpath))).click()

    @allure.step("Выбрать сортировку: {sort_type}")
    def select_sort_type(self, sort_type: str) -> None:
        """Выбирает опцию сортировки"""
        self.wait_for_element(self.sort_dropdown)
        self.__driver.find_element(By.CSS_SELECTOR, self.sort_dropdown).click()

        sort_text = self.sort_options.get(sort_type, sort_type)
        option_xpath = (
            f'//div[contains(@role, "option") '
            f'and contains(text(), "{sort_text}")]'
        )
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, option_xpath))).click()

    @allure.step("Получить названия товаров на странице")
    def get_item_names(self) -> list:
        """Возвращает список названий товаров на странице"""
        self.wait_for_element(self.item_cards)
        items = self.__driver.find_elements(By.CSS_SELECTOR, self.item_title)
        return [i.text for i in items]

    @allure.step("Открыть карточку первого товара в каталоге")
    def open_item_card(self) -> str:
        """Открывает карточку первого товара и возвращает его название"""
        first_item = self.__driver.find_element(
            By.CSS_SELECTOR, self.item_cards)
        first_item_title = first_item.find_element(
            By.CSS_SELECTOR, self.first_item_title).text
        first_item.find_element(By.CSS_SELECTOR, self.item_image).click()

        return first_item_title

    @allure.step("Проверить, что открыта страница товара")
    def item_page_is_opened(self) -> bool:
        """Проверяет, что открыта страница детального просмотра товара"""
        self.wait_for_element(self.item_info)
        return True

    @allure.step("Добавить первый товар из каталога в корзину")
    def add_first_item_to_cart_from_catalog(self) -> str:
        """
        Добавляет первый товар в корзину со страницы каталога.
        Наводит на изображение, ждет появления кнопки корзины, нажимает,
        выбирает первый доступный размер.
        Возвращает название товара.
        """
        first_item = self.__driver.find_element(
            By.CSS_SELECTOR, self.item_cards)
        first_item_title = first_item.find_element(
            By.CSS_SELECTOR, self.first_item_title).text

        ActionChains(self.__driver).move_to_element(first_item).perform()

        cart_button = first_item.find_element(
            By.CSS_SELECTOR, self.cart_button)
        self.wait.until(EC.element_to_be_clickable(cart_button)).click()

        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.size_modal)))

        sizes = self.__driver.find_elements(By.CSS_SELECTOR, self.size_modal)
        for size in sizes:
            if "text-middle-gray" not in size.get_attribute("class"):
                size.click()
                break

        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.cart_modal)))
        return first_item_title

    @allure.step("Проверить, что товар {item_name} есть в корзине")
    def item_is_in_cart(self, item_name: str) -> bool:
        """Проверяет наличие товара в корзине по названию"""
        items = self.__driver.find_elements(
            By.CSS_SELECTOR, self.cart_item_title)
        for item in items:
            if item_name in item.text:
                return True
