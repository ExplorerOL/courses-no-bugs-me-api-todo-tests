from requests import Response

from api.requests.crud_interface import CRUDInterface
from api.requests.request import Request
from config.endpoints import Endpoints


class ToDoRequest(Request, CRUDInterface):
    def read_all(self) -> Response:
        return self.__http_session.get(self.__base_url + Endpoints.todos)

    def create(self, data) -> Response:
        return self.__http_session.post(self.__base_url + Endpoints.todos, json=data)

    def read(self, id) -> Response:
        pass

    def update(self, id, data) -> Response:
        pass

    def delete(self, id) -> Response:
        pass
