from typing import Optional


class Singleton:
    __instance: Optional['Singleton'] | None = None

    @staticmethod
    def __new__(cls):
        if Singleton.__instance is None:
            Singleton.__instance = super().__new__(cls)
            return Singleton.__instance
        else:
            return Singleton.__instance
