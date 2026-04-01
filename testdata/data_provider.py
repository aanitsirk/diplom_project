import json

with open('testdata/test_data.json') as f:
    global_data = json.load(f)


class DataProvider:

    def __init__(self) -> None:
        self.data = global_data

    def get_email(self) -> str:
        return self.data.get("email", "")

    def get_password(self) -> str:
        return self.data.get("password", "")
