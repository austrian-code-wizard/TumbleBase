from util.utils import get_config_parser
import requests


class twWebConnector:
    def __init__(self):
        config_parser = get_config_parser("environment.ini")
        self._host = str(config_parser["tumbleWebServer"]["host"])
        self._port = str(config_parser["tumbleWebServer"]["port"])
        self._route = str(config_parser["tumbleWebServer"]["route"])

    def send(self, json_data):
        result = requests.post(f"http://{self._host}:{self._port}{self._route}", json=json_data)
        return result.json()["data"]

