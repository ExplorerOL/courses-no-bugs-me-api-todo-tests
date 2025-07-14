import json
from dataclasses import asdict
from http import HTTPStatus

import pytest

from config.endpoints import Endpoints
from src.models.todo import ToDo
from testrunner.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestGetTodos(BaseTest):
    def test_create_todo_with_valid_data(self):
        new_todo = ToDo(id=1, text='New Task', completed=False)

        response = self.http_session.post(
            url=self.base_url + Endpoints.todos,
            data=json.dumps(asdict(new_todo)),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.text == ''
        response = self.http_session.get(url=self.base_url + Endpoints.todos)
