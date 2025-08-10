from abc import abstractmethod
from typing import Any, TypeVar

from support.reporters.allure.reporter_metaclasses import (
    MetaclassWithMethodReporting,
)

T = TypeVar('T')


class CRUDInterface(metaclass=MetaclassWithMethodReporting):
    @abstractmethod
    def create(self, data: T) -> T: ...

    @abstractmethod
    def update(self, id: int, data: T) -> T: ...

    @abstractmethod
    def delete(self, id: int) -> Any: ...
