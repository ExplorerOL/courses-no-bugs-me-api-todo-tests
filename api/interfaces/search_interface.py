from abc import abstractmethod
from typing import overload

from models.todo import ToDo
from support.reporters.allure.reporter_metaclasses import (
    MetaclassWithMethodReporting,
)


class SearchInterface(metaclass=MetaclassWithMethodReporting):
    @abstractmethod
    @overload
    def read_all(self) -> list[ToDo]: ...

    @abstractmethod
    def read_all(self, offset: int, linit: int) -> list[ToDo]: ...
