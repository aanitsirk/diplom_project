# diplom_project
Репозиторий для дипломной работы по автоматизированному тестированию интернет-магазина [zarina.ru](https://zarina.ru).  

Проект включает UI и API тесты с использованием PageObject, Allure отчетов и интеграцией с GitHub.

## Шаги для запуска

1. Склонировать проект: `git clone https://github.com/aanitsirk/diplom_project.git`
2. Установить зависимости: `pip install -r requirements.txt`
3. Запустить все тесты: `pytest -v`
- Запустить UI тесты: `pytest -m ui -v`
- Запустить API тесты: `pytest -m api -v`
4. Сгенерировать отчет `allure generate allure-results -o allure-report`
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
    - MainPage.py            # главная страница
    - CatalogPage.py         # страница каталога
- ./api/                     # хелперы для работы с API
    - api_client.py          # клиент для API запросов
- ./config/                  # провайдер настроек
    - settings.py            # настройки проекта
- ./testdata/                # провайдер тестовых данных
    - test_data.json         # тестовые данные
    - data_provider.py       # загрузка тестовых данных
- allure-results/            # результаты тестов для Allure
- allure-report/             # сгенерированный отчет Allure
- .gitignore                 # исключения для Git
- requirements.txt           # зависимости проекта
- pytest.ini                 # настройки pytest
- README.md                  # документация

#### Особенности проекта

1. UI тесты используют PageObject паттерн для организации кода
2. API тесты работают с реальными эндпоинтами интернет-магазина
3. Allure отчеты содержат шаги тестов, скриншоты и вложения
4. Тестовые данные вынесены в отдельные файлы и не хранятся в коде
5. Маркеры позволяют запускать тесты выборочно (pytest -m ui, pytest -m api)

##### Ссылка на финальный проект

https://kristinamaslova.yonote.ru/share/d5ed6fb6-5ec5-4e24-a3a5-b35b82903fbd