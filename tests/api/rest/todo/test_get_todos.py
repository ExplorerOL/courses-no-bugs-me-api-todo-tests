from dataclasses import asdict

import pytest

# from api.requests.todo_request import TodoRequest
from api.requests.todo_request import ToDoRequest
from api.rest.models.models import ToDo
from config.endpoints import Endpoints
from testrunner.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestGetTodos(BaseTest):
    def test_get_todos_with_empty_db(self):
        """Получение пустого списка TODO при пустой БД"""
        response = self.http_session.get(url=self.base_url + Endpoints.todos)

        assert response.status_code == 200
        body = response.json()
        assert len(body) == 0

    def test_create_todo(self):
        response = ToDoRequest(
            base_url=self.base_url,
        ).create(data=asdict(ToDo(id=1, text='test1', completed=False)))
        print(f'{response!r}')

    def test_get_todos_with_not_empty_db(self):
        todo1 = ToDo(id=1, text='test1', completed=False)
        todo2 = ToDo(id=2, text='test2', completed=False)

        self.create_todo(todo1)
        self.create_todo(todo2)

        response = self.http_session.get(url=self.base_url + Endpoints.todos)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        body = response.json()
        assert len(body) == 2
