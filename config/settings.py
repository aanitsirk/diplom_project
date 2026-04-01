import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    base_url = "https://zarina.ru"
    api_base_url = "https://api.zarina.ru/api"

    email = os.getenv("email", "religious96@sharebot.net")
    password = os.getenv("password", "E7E8EGKyiC!7jeF")

    implicity_wait = 5
    cookies_file = "cookies.pkl"


settings = Settings()
