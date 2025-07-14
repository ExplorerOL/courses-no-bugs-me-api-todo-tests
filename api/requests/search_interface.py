from abc import ABC, abstractmethod
from typing import Any, TypeVar, overload


class SearchInterface(ABC):
    @abstractmethod
    @overload
    def read_all(self) -> Any: ...

    # @abstractmethod
    # @overload
    # def read_all(self, offset: int, linit: int) -> Any: ...
