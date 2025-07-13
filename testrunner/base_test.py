# from api.requests.request import HTTPSession
import json

import pytest
import requests
import requests.auth

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

    @pytest.fixture(scope='function')
    def delete_all_todos(self) -> None:
        todos_response = self.http_session.get(url=self.base_url + '/todos')
        todos = json.loads(todos_response.content)
        for todo in todos:
            print(todo)
            self.http_session.delete(url=self.base_url + Endpoints.todo_by_id.format(todo_id=str(todo['id'])))
