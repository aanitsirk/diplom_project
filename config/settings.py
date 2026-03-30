import json
import configparser
import os

_config = configparser.ConfigParser()
_config.read("config/test_config.ini")

ui_base_url = __config.get("ui", "base_url")
ui_timeout = __config.getint("ui", "timeout")

api_base_url = __config.get("api", "base_url")
api_timeout = __config.getint("api", "timeout")

class ConfigProvider:

    def __init__(self) -> None:
        self.config = global_config

    def get(self, section: str, prop: str):
        return self.config[section].get(prop)

    def getint(self, section: str, prop: str):
        return self.config[section].getint(prop)

    def get_ui_url(self):
        return self.config["ui"].get('base_url')


load_dotenv()


class Settings:
    base_url = "https://zarina.ru"
    api_base_url = "https://api.zarina.ru"

    email = os.getenv("email", "religious96@sharebot.net")
    password = os.getenv("password", "E7E8EGKyiC!7jeF")

    implicity_wait = 5

    cookies_file = "cookies.pkl"


settings = Settings()
