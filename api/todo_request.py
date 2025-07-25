import json
from dataclasses import asdict

from requests import Response

from api.api_request import APISession
from api.interfaces.crud_interface import CRUDInterface
from config.endpoints import Endpoints
from models.todo import ToDo
from support.reporters.allure.reporter_base_classes import ClassWithMethodReporting
from support.reporters.allure.reporter_metaclasses import MetaclassABCMetaWithMethodReporting


class ToDoRequest(
    CRUDInterface,
    ClassWithMethodReporting,
    metaclass=MetaclassABCMetaWithMethodReporting,
):
    def __init__(self, api_session: APISession):
        self._api_request = api_session

    def create(self, data: ToDo) -> Response:
        return self._api_request.session.post(
            self._api_request.base_url + str(Endpoints.TODOS.value),
            json=asdict(data),
            headers={'Content-Type': 'application/json'},
        )

    def update(self, id, data: ToDo) -> Response:
        return self._api_request.session.put(
            url=self._api_request.base_url + str(Endpoints.TODO_BY_ID.value).format(todo_id=id),
            data=json.dumps(asdict(data)),
            headers={'Content-Type': 'application/json'},
        )

    def delete(self, id) -> Response:
        return self._api_request.session.delete(
            url=self._api_request.base_url + str(Endpoints.TODO_BY_ID.value).format(todo_id=id)
        )

    def read_all(self, offset: int | None = None, limit: int | None = None) -> Response:
        if all([offset is not None, limit is not None]):
            return self._api_request.session.get(
                self._api_request.base_url + str(Endpoints.TODOS.value),
                params={'offset': offset, 'limit': limit},
            )
        else:
            return self._api_request.session.get(self._api_request.base_url + str(Endpoints.TODOS.value))
