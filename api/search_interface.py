from abc import ABC, abstractmethod
from typing import overload

from models.todo import ToDo


class SearchInterface(ABC):
    @abstractmethod
    @overload
    def read_all(self) -> list[ToDo]: ...

    @abstractmethod
    def read_all(self, offset: int, linit: int) -> list[ToDo]: ...
