# diplom_project
Репозиторий для дипломной работы по автоматизированному тестированию интернет-магазина [zarina.ru](https://zarina.ru).  

Проект включает UI и API тесты с использованием PageObject, Allure отчетов и поддержкой работы с БД.

## Шаги для запуска

1. Склонировать проект: `git clone https://github.com/aanitsirk/diplom_project.git`
2. Установить зависимости: `pip install -r requirements.txt`
3. Запустить все тесты: `pytest`
4. Сгенерировать отчет `allure generate allure-files -o allure-report`
5. Открыть отчет `allure open allure-report`

### Стек

- pytest - фреймворк для написания и запуска тестов
- selenium - автоматизация взаимодействия с веб-браузером
- requests - выполнение HTTP-запросов для API тестирования
- allure - формирование отчетов о тестировании
- configparser - чтение конфигурационных файлов
- json - работа с тестовыми данными в формате JSON
- webdriver-manager - автоматическое управление драйверами браузеров

### Структура проекта

- ./tests/                   # тесты
    - test_ui.py             # UI тесты
    - test_api.py            # API тесты
    - conftest.py            # фикстуры pytest
- ./pages/                   # описание страниц (PageObject)
    - main_page.py           # главная страница
    - catalog_page.py        # страница каталога
    - cart_page.py           # страница корзины
- ./api/                     # хелперы для работы с API
    - client.py              # базовый клиент для API запросов
    - endpoints.py           # эндпоинты API
- ./config/                  # провайдер настроек
    - settings.py            # чтение конфигурации
    - test_config.ini        # настройки для тестов
- ./testdata/                # провайдер тестовых данных
    - test_data.json         # тестовые данные
    - data_provider.py       # загрузка тестовых данных
- ./utils/                   # вспомогательные утилиты
    - cookies_helper.py      # работа с cookies
- allure-results/            # результаты тестов для Allure
- allure-report/             # сгенерированный отчет Allure
- .gitignore                 # исключения для Git
- requirements.txt           # зависимости проекта
- pytest.ini                 # настройки pytest
- README.md                  # документация