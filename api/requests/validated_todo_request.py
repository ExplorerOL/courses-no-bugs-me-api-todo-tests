from http import HTTPStatus
from typing import overload

from requests import Response

from api.requests.crud_interface import CRUDInterface
from api.requests.request import Request
from api.requests.search_interface import SearchInterface
from api.requests.todo_request import ToDoRequest
from config.endpoints import Endpoints


class ValidatedToDoRequest(Request, CRUDInterface, SearchInterface):
    def __init__(self, base_url, http_session):
        super().__init__(base_url=base_url, http_session=http_session)
        self.__todo_request = ToDoRequest(base_url=self.__base_url, http_session=self.__http_session)

    def create(self, data) -> str:
        response = self.__todo_request.create(data)
        assert response.status_code == HTTPStatus.CREATED
        return response.text

    @overload
    def read_all(self) -> Response:
        response = self.__todo_request.read_all()
        assert response.status_code == HTTPStatus.OK
        return response.json()

    @overload
    def read_all(self, limit, offset) -> Response:
        response = self.__http_session.get(self.__base_url + Endpoints.todos)
        assert response.status_code == HTTPStatus.OK
        return response.json()
