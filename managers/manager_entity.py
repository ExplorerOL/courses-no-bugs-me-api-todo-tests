from typing import TypeVar

from api.interfaces.crud_interface import CRUDInterface
from support.reporters.allure.reporter_base_classes import ClassWithMethodReporting

T = TypeVar('T')


class ManagerEntity(ClassWithMethodReporting):
    _storage: dict[T] = {}
    _entity_crud: CRUDInterface

    def __init__(self, entity_crud: CRUDInterface):
        self._entity_crud = entity_crud

    @property
    def storage(self) -> dict[T]:
        return self._storage

    def add_data(self, data: T) -> None:
        """Добавление данных в хранилище"""
        self._storage[data.id] = data

    def remove_data(self, id: int) -> None:
        """Удаление данных из хранилища"""
        self._storage.pop(id, None)

    def clean_storage(self) -> None:
        """Очистка хранилища"""
        self._storage = {}

    def create_entity(self, data: T) -> None:
        """Создание сущности"""
        self._entity_crud.create(data=data)

    def delete_entity(self, id: int) -> None:
        """Удаление сущности"""
        self._entity_crud.delete(id=id)

    def delete_all_entities(self) -> None:
        """Удаление всех сущностей"""
        ids = list(self._storage.keys())
        for id in ids:
            try:
                self._entity_crud.delete(id=id)
            except AssertionError:
                pass
        self.clean_storage()
