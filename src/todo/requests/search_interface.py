from abc import ABC, abstractmethod

from src.models.todo import ToDo


class SearchInterface(ABC):
    @abstractmethod
    def read_all(self, offset: int | None = None, linit: int | None = None) -> list[ToDo]: ...
