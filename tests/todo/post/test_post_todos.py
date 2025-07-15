import json
from dataclasses import asdict
from http import HTTPStatus

import pytest

from src.models.todo import ToDo
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestPostTodos(BaseTest):
    def test_create_todo_with_valid_data(self):
        new_todo = ToDo(id=1, text='New Task', completed=False)

        response = self.http_session.post(
            url=self.base_url + '/todos',
            data=json.dumps(asdict(new_todo)),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.text == ''

        response = self.http_session.get(url=self.base_url + '/todos')
        body = response.json()

        found = False
        for todo in body:
            if todo.get('id') == new_todo.id:
                assert todo.get('text') == new_todo.text
                assert todo.get('completed') is False
                found = True
                break
        assert found, 'Созданная задача не найдена в списке TODO'

    def test_create_todo_with_missing_fialds(self):
        new_todo = {'id': 2, 'completed': True}

        response = self.http_session.post(
            url=self.base_url + '/todos',
            data=json.dumps(new_todo),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.headers.get('Content-Type') == 'text/plain; charset=utf-8'
        assert response.text

    def test_create_todo_with_max_length_text(self):
        max_length_text = ''.join('A' for i in range(255))
        new_todo = ToDo(id=3, text=max_length_text, completed=False)

        response = self.http_session.post(
            url=self.base_url + '/todos',
            data=json.dumps(asdict(new_todo)),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.text == ''

        response = self.http_session.get(url=self.base_url + '/todos')
        assert response.status_code == HTTPStatus.OK
        body = response.json()

        found = False
        for todo in body:
            if todo.get('id') == new_todo.id:
                assert todo.get('text') == new_todo.text
                assert todo.get('completed') is False
                found = True
                break
        assert found, 'Созданная задача не найдена в списке TODO'

    def test_create_todo_with_invalid_data_types(self):
        new_todo = {'id': 4, 'text': 'Invalid Data Typ', 'completed': 'notBoolean'}

        response = self.http_session.post(
            url=self.base_url + '/todos',
            data=json.dumps(new_todo),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.text

    def test_create_todo_with_existing_id(self):
        first_todo = ToDo(id=5, text='First Task', completed=False)
        self.create_todo(todo_data=first_todo)

        duplicated_todo = ToDo(id=5, text='Duplicated Task', completed=True)

        response = self.http_session.post(
            url=self.base_url + '/todos',
            data=json.dumps(asdict(duplicated_todo)),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.text == ''
