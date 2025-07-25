from typing import Optional

from support.reporters.allure.reporter_allure import ReporterAllure
from support.reporters.allure.reporter_protocol import ReporterProtocol


class ConfigGeneral:
    """Конфигурация тестов. Испоользуется паттерн Singleton"""

    __instance: Optional['ConfigGeneral'] = None
    __base_url: str = 'http://192.168.0.4:8080'
    __timeout_ms: int = 10000
    __version: str = ''
    __reporter = ReporterAllure()

    @staticmethod
    def __new__(cls):
        if ConfigGeneral.__instance is None:
            ConfigGeneral.__instance = super().__new__(cls)
        return ConfigGeneral.__instance

    @property
    def base_url(self) -> str:
        return self.__base_url

    @base_url.setter
    def base_url(self, new_base_url: str) -> None:
        self.__base_url = new_base_url

    @property
    def timeout_ms(self) -> int:
        return self.__timeout_ms

    def get_version(self) -> str:
        return self.__version

    def set_version(self, version: str) -> None:
        self.__version = version

    @property
    def reporter(self) -> ReporterProtocol:
        return self.__reporter


config_general = ConfigGeneral()
