from typing import Optional

from api.todo_requester import todo_requester
from managers.manager_entity import ManagerEntity
from models.todo import ToDo
from support.event_bus.event_bus import event_bus


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
event_bus.subscribe('todo.created', lambda data: manager_todo.add_data(data=data))
event_bus.subscribe('todo.deleted', lambda id: manager_todo.remove_data(id=id))
