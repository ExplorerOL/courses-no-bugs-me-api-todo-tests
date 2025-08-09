from abc import ABC, abstractmethod

from models.todo import ToDo


class NotificationInterface(ABC):
    @abstractmethod
    def read_all(self) -> ToDo: ...
