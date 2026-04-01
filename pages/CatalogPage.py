import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from config.settings import settings
from pages.MainPage import MainPage


class CatalogPage:

    item_cards = '.catalog-item'
    item_info = '.product-info'
    item_image = 'img[alt="image"]'

    first_item_title = '.product-title a'
    cart_button = '.product-cart img[alt="Cart"]'
    size_modal = '.flex.flex-col.items-center.gap-2'

    cart_item_title = '.flex-1.space-y-2 h3'

    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        self.__url = f'{settings.base_url}/catalog/clothes/'
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element(self, selector: str) -> None:
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, selector)))

    @allure.step("Открыть страницу каталога через главную страницу")
    def open_catalog(self) -> None:
        """Открывает страницу каталога"""
        main_page = MainPage(self.__driver)
        main_page.open()
        main_page.click_menu_burger()
        main_page.go_to_women_catalog()

        main_page.accept_city_modal()

        self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, self.item_cards)))

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
        items = self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, self.item_cards)))
        first_item = items[0]
        first_item_title = first_item.find_element(
            By.CSS_SELECTOR, self.first_item_title).text

        image_hover = first_item.find_element(By.CSS_SELECTOR, self.item_image)
        ActionChains(self.__driver).move_to_element(image_hover).perform()

        cart_button = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, self.cart_button)))
        cart_button.click()

        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.size_modal)))

        sizes = self.__driver.find_elements(By.CSS_SELECTOR, self.size_modal)
        for size in sizes:
            if "bg-black" not in size.get_attribute("class"):
                size.click()
                break

        return first_item_title

    @allure.step("Проверить, что товар {item_name} есть в корзине")
    def item_is_in_cart(self, item_name: str) -> str:
        """Проверяет наличие товара в корзине по названию"""
        items = self.__driver.find_elements(
            By.CSS_SELECTOR, self.cart_item_title)
        for item in items:
            if item_name.lower() in item.text.lower():
                return item.text
