from abc import abstractmethod

from models.todo import ToDo
from support.reporters.allure.reporter_metaclasses import (
    MetaclassWithMethodReporting,
)


class NotificationInterface(metaclass=MetaclassWithMethodReporting):
    @abstractmethod
    def read_all(self) -> ToDo: ...
