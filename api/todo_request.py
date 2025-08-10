import json
from dataclasses import asdict
from http import HTTPStatus

from requests import Response

from api.interfaces.crud_interface import CRUDInterface
from api.rest.rest_request import RESTRequest
from config.endpoints import Endpoints
from models.todo import ToDo
from support.event_bus.event_bus import event_bus


class ToDoRequest(CRUDInterface):
    def __init__(self, rest_request: RESTRequest):
        self._api_request = rest_request

    def create(self, data: ToDo) -> Response:
        """Отправка запроса на создание"""
        response = self._api_request.session.post(
            self._api_request.base_url + str(Endpoints.TODOS.value),
            json=asdict(data),
            headers={'Content-Type': 'application/json'},
        )
        if response.status_code == HTTPStatus.CREATED:
            event_bus.publish('todo.created', data=data)
        return response

    def update(self, id, data: ToDo) -> Response:
        """Отправка запроса на обновление"""
        response = self._api_request.session.put(
            url=self._api_request.base_url + str(Endpoints.TODO_BY_ID.value).format(todo_id=id),
            data=json.dumps(asdict(data)),
            headers={'Content-Type': 'application/json'},
        )
        if response.status_code == HTTPStatus.OK:
            event_bus.publish('todo.created', data=data)
        return response

    def delete(self, id) -> Response:
        """Отправка запроса на удаление"""
        response = self._api_request.session.delete(
            url=self._api_request.base_url + str(Endpoints.TODO_BY_ID.value).format(todo_id=id)
        )
        if response.status_code == HTTPStatus.OK:
            event_bus.publish('todo.deleted', id=id)
        return response

    def read_all(self, offset: int | None = None, limit: int | None = None) -> Response:
        """Отправка запроса на чтение всех записей"""
        if all([offset is not None, limit is not None]):
            return self._api_request.session.get(
                self._api_request.base_url + str(Endpoints.TODOS.value),
                params={'offset': offset, 'limit': limit},
            )
        else:
            return self._api_request.session.get(self._api_request.base_url + str(Endpoints.TODOS.value))
