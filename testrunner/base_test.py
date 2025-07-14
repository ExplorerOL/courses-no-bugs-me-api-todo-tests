# from api.requests.request import HTTPSession
import json
from dataclasses import asdict

import pytest
import requests
import requests.auth

from api.rest.models.models import ToDo
from config.endpoints import Endpoints
from data.creds import auth_user_creds


class BaseTest:
    __URL = 'http://192.168.0.4'
    __PORT = 8080
    __http_session = requests.Session()
    __http_session.auth = (auth_user_creds.username, auth_user_creds.password)

    @property
    def http_session(self):
        return self.__http_session

    @property
    def base_url(self):
        return f'{self.__URL}:{self.__PORT}'

    def create_todo(self, data: ToDo) -> None:
        self.http_session.post(
            url=self.base_url + Endpoints.todos,
            data=json.dumps(asdict(data)),
            headers={'Content-Type': 'application/json'},
        )

    def delete_all_todos(self) -> None:
        todos_response = self.http_session.get(url=self.base_url + Endpoints.todos)
        todos = json.loads(todos_response.content)
        for todo in todos:
            self.http_session.delete(url=self.base_url + Endpoints.todo_by_id.format(todo_id=todo['id']))

    @pytest.fixture(scope='function')
    def delete_all_todos_scope_test(self) -> None:
        self.delete_all_todos()
