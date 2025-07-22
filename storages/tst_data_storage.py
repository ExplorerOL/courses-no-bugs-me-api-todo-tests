from typing import Optional

from models.todo import ToDo


class TstDataStorage:
    __instance: Optional['TstDataStorage'] = None
    __storage: dict[ToDo] = {}

    @staticmethod
    def __new__(cls):
        if TstDataStorage.__instance is None:
            TstDataStorage.__instance = super().__new__(cls)
            return TstDataStorage.__instance
        else:
            return TstDataStorage.__instance

    @property
    def storage(self) -> dict[ToDo]:
        return self.__storage

    def add_data(self, data: ToDo) -> None:
        self.__storage[data.id] = data

    def clean(self) -> None:
        self.__storage = {}
