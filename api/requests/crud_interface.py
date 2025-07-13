from abc import ABC
from typing import TypeVar

T = TypeVar('T')


class CRUDInterface(ABC):
    def create(self, data: T) -> T: ...
    def update(self, id: int, data: T) -> T: ...
    def delete(self, id: int) -> T: ...
