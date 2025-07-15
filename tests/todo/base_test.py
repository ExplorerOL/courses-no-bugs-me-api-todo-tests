# from src.requests.request import HTTPSession
import json
from dataclasses import asdict

import requests

from src.models.todo import ToDo


class BaseTest:
    __URL = 'http://192.168.0.4'
    __PORT = 8080
    _http_session = requests.Session()

    # todo_request = ToDoRequest(
    #         base_url=BaseTest.base_url,
    #         auth_creds=(
    #             auth_user_creds.username,
    #             auth_user_creds.password,
    #         ),
    #     )
    #     self._validated_todo_request = ValidatedToDoRequest()

    @property
    def http_session(self):
        return self._http_session

    # @property
    # def todo_request(self):
    #     return self._todo_request

    # @property
    # def validated_todo_request(self):
    #     return self._validated_todo_request

    @property
    def base_url(self):
        return f'{self.__URL}:{self.__PORT}'

    # TODO: удалить
    def create_todo(self, todo_data: ToDo) -> None:
        self.http_session.post(
            url=self.base_url + '/todos',
            data=json.dumps(asdict(todo_data)),
            headers={'Content-Type': 'application/json'},
        )

    # TODO: удалить
    def delete_all_todos(self) -> None:
        todos_response = self.http_session.get(url=self.base_url + '/todos')
        todos = json.loads(todos_response.content)
        for todo in todos:
            self.http_session.delete(
                url=self.base_url + '/todos/' + str(todo['id']),
                auth=('admin', 'admin'),
            )
