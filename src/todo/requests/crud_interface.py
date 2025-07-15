from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar('T')


class CRUDInterface(ABC):
    @abstractmethod
    def create(self, data: T) -> T: ...

    @abstractmethod
    def update(self, id: int, data: T) -> T: ...

    @abstractmethod
    def delete(self, id: int) -> Any: ...
