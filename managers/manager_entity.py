from typing import TypeVar

from api.interfaces.crud_interface import CRUDInterface

T = TypeVar('T')


class ManagerEntity:
    _storage: dict[T] = {}
    _entity_crud: CRUDInterface

    def __init__(self, entity_crud: CRUDInterface):
        self._entity_crud = entity_crud

    @property
    def storage(self) -> dict[T]:
        return self._storage

    def add_data(self, data: T) -> None:
        self._storage[data.id] = data

    def remove_data(self, id: int) -> None:
        self._storage.pop[id]

    def clean_storage(self) -> None:
        self._storage = {}

    def create_entity(self, data: T) -> None:
        self._entity_crud.create(data=data)
        self.add_data(data=data)

    def delete_entity(self, id: int) -> None:
        self._entity_crud.delete(id=id)
        self.remove_data(id=id)

    def delete_all_entities(self) -> None:
        for id in self._storage.keys():
            try:
                self._entity_crud.delete(id=id)
            except AssertionError:
                pass
        self.clean_storage()
