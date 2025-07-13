from requests import Response

from api.requests.request import Request


class ToDoRequest(Request):
    def create(self, data) -> Response:
        return self.__http_session.post(self.__http_session.base_url + '/todos', json=data)

    def read_all(self) -> Response:
        return self.__http_session.get(self.__http_session.base_url + '/todos')
