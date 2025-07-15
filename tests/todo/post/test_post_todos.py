import json
from dataclasses import asdict
from http import HTTPStatus

import pytest

from config.endpoints import Endpoints
from src.models.todo import ToDo
from testrunner.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestPostTodos(BaseTest):
    def test_update_existing_todo_with_valid_data(self):
        new_todo = ToDo(id=1, text='Original Task', completed=False)
        self.create_todo(todo_data=new_todo)
        updated_todo = ToDo(id=1, text='Updated Task', completed=True)

        response = self.http_session.post(
            url=self.base_url + Endpoints.todos,
            data=json.dumps(asdict(new_todo)),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.text == ''

        response = self.http_session.get(url=self.base_url + Endpoints.todos)
        body = response.json()

        found = False
        for todo in body:
            if todo.get('id') == new_todo.id:
                assert todo.get('text') == new_todo.text
                assert todo.get('completed') is False
                found = True
                break
        assert found, 'Созданная задача не найдена в списке TODO'
