from typing import Optional

from api.todo_requester import todo_requester
from managers.manager_entity import ManagerEntity
from models.todo import ToDo


class ManagerToDo(ManagerEntity):
    __instance: Optional['ManagerToDo'] = None
    __storage: dict[ToDo] = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ManagerToDo, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, entity_crud):
        if not self.__initialized:
            self._entity_crud = entity_crud
            self.__initialized = True


manager_todo = ManagerToDo(entity_crud=todo_requester.validated_todo_request_admin)
