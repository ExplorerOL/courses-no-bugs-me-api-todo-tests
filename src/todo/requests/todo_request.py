import json
from dataclasses import asdict

from requests import Response

from config.endpoints import Endpoints
from src.models.todo import ToDo
from src.todo.requests.crud_interface import CRUDInterface
from src.todo.requests.request import Request
from src.todo.requests.search_interface import SearchInterface


class ToDoRequest(CRUDInterface, SearchInterface, Request):
    def create(self, data: ToDo) -> Response:
        return self._http_session.post(
            self._base_url + Endpoints.todos,
            json=asdict(data),
            headers={'Content-Type': 'application/json'},
        )

    def update(self, id, data: ToDo) -> Response:
        return self._http_session.put(
            url=self._base_url + Endpoints.todo_by_id.format(todo_id=id),
            data=json.dumps(
                data,
                headers={'Content-Type': 'application/json'},
            ),
        )

    def delete(self, id) -> Response:
        return self._http_session.delete(url=self._base_url + Endpoints.todo_by_id.format(todo_id=id))

    def read_all(self, offset: int | None = None, limit: int | None = None) -> Response:
        if all([offset is not None, limit is not None]):
            return self._http_session.get(
                self._base_url + Endpoints.todos,
                params={'offset': offset, 'limit': limit},
            )
        else:
            return self._http_session.get(self._base_url + Endpoints.todos)
