from abc import ABC, abstractmethod
from typing import Any


class SearchInterface(ABC):
    @abstractmethod
    def read_all(self, offset: int | None = None, linit: int | None = None) -> Any: ...
