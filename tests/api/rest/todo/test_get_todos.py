from dataclasses import asdict
import json
import pytest

# from api.requests.todo_request import TodoRequest
from api.requests.todo_request import ToDoRequest
from api.rest.models.models import ToDo
from config.endpoints import Endpoints
from testrunner.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestGetTodos(BaseTest):
    def test_get_todos_with_existing_entries(self):
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
