from abc import ABC, abstractmethod
from typing import Any, TypeVar, overload


class SearchInterface(ABC):
    @abstractmethod
    @overload
    def readAll(self) -> Any: ...

    @abstractmethod
    @overload
    def readAll(self, offset: int, linit: int) -> Any: ...
