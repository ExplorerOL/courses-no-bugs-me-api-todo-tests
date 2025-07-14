import json
from typing import overload

from requests import Response

from api.requests.crud_interface import CRUDInterface
from api.requests.request import Request
from api.requests.search_interface import SearchInterface
from api.rest.models.models import ToDo
from config.endpoints import Endpoints


class ToDoRequest(CRUDInterface, SearchInterface, Request):
    @overload
    def read_all(self) -> Response:
        return self._http_session.get(self._base_url + Endpoints.todos)

    @overload
    def read_all(self, offset: int, limit: int) -> Response:
        return self.__http_session.get(
            self.__base_url + Endpoints.todos,
            params={'offset': offset, 'limit': limit},
        )

    def create(self, data) -> Response:
        return self._http_session.post(
            self._base_url + Endpoints.todos,
            json=data,
        )

    def update(self, id, data: ToDo) -> Response:
        return self._http_session.put(
            url=self._base_url + Endpoints.todo_by_id.format(todo_id=id), data=json.dumps(data)
        )

    def delete(self, id) -> Response:
        return self._http_session.delete(url=self._base_url + Endpoints.todo_by_id.format(todo_id=id))
