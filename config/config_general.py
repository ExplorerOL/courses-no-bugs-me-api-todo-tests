from typing import Optional


class ConfigGeneral:
    """Конфигурация тестов. Испоользуется паттерн Singleton"""

    __instance: Optional['ConfigGeneral'] | None = None
    __base_url: str = 'http://192.168.0.4:8080'

    @staticmethod
    def __new__(cls):
        if ConfigGeneral.__instance is None:
            ConfigGeneral.__instance = super().__new__(cls)
            return ConfigGeneral.__instance
        else:
            return ConfigGeneral.__instance

    @property
    def base_url(self) -> str:
        return self.__base_url

    @base_url.setter
    def base_url(self, new_base_url: str) -> None:
        self.__base_url = new_base_url


config_general = ConfigGeneral()
