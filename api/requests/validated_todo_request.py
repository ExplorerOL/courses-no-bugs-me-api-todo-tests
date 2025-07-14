from http import HTTPStatus
from typing import overload

from api.requests.crud_interface import CRUDInterface
from api.requests.request import Request
from api.requests.search_interface import SearchInterface
from api.requests.todo_request import ToDoRequest
from api.rest.models.models import ToDo


class ValidatedToDoRequest(Request, CRUDInterface, SearchInterface):
    def __init__(self, base_url, http_session):
        super().__init__(base_url=base_url, http_session=http_session)
        self.__todo_request = ToDoRequest(base_url=self._base_url, http_session=self._http_session)

    def create(self, data) -> str:
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

    @overload
    def read_all(self) -> list[ToDo]:
        response = self.__todo_request.read_all()
        assert response.status_code == HTTPStatus.OK
        body_json = response.json()
        return [ToDo(**todo) for todo in body_json]
