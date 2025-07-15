from http import HTTPStatus
from typing import overload

from src.models.creds import CredsUsernamePassword
from src.models.todo import ToDo
from src.todo.requests.crud_interface import CRUDInterface
from src.todo.requests.request import Request
from src.todo.requests.search_interface import SearchInterface
from src.todo.requests.todo_request import ToDoRequest


class ValidatedToDoRequest(Request, CRUDInterface, SearchInterface):
    def __init__(self, base_url: str, auth_creds: CredsUsernamePassword | None = None):
        super().__init__(base_url=base_url, auth_creds=auth_creds)
        self.__todo_request = ToDoRequest(base_url=self._base_url, auth_creds=self._auth_creds)

    def create(self, data: ToDo) -> str:
        response = self.__todo_request.create(data=data)
        assert response.status_code == HTTPStatus.CREATED
        return response.text

    def update(self, id: int, data: ToDo) -> ToDo:
        response = self.__todo_request.update(id=id, data=data)
        assert response.status_code == HTTPStatus.OK
        body_json = response.json()
        return ToDo(**body_json)

    def delete(self, id: int) -> str:
        response = self.__todo_request.delete(id=id)
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response.text

    @overload
    def read_all(self, limit, offset) -> list[ToDo]:
        response = self.__todo_request.read_all(limit=limit, offset=offset)
        assert response.status_code == HTTPStatus.OK
        body_json = response.json()
        return [ToDo(**todo) for todo in body_json]

    def read_all(self) -> list[ToDo]:
        response = self.__todo_request.read_all()
        assert response.status_code == HTTPStatus.OK
        body_json = response.json()
        return [ToDo(**todo) for todo in body_json]
