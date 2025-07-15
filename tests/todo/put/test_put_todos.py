import json
from dataclasses import asdict
from http import HTTPStatus

import pytest

from src.models.todo import ToDo
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestPutTodos(BaseTest):
    def test_update_existing_todo_with_valid_data(self):
        """Обновление существующего TODO корректными данными"""
        original_todo = ToDo(id=1, text='Original Task', completed=False)
        self.create_todo(original_todo)

        updated_todo = ToDo(id=1, text='Updated Task', completed=True)

        response = self.http_session.put(
            url=self.base_url + '/todos/' + str(updated_todo.id),
            data=json.dumps(asdict(updated_todo)),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.OK

        response = self.http_session.get(url=self.base_url + '/todos')
        assert response.status_code == HTTPStatus.OK
        body = response.json()

        assert len(body) == 1
        assert body[0].get('text') == 'Updated Task'
        assert body[0].get('completed') is True

    def test_update_non_existing_todo(self):
        """Попытка обновления TODO с несуществующим id"""
        updated_todo = ToDo(id=999, text='Non-existent Task', completed=True)

        response = self.http_session.put(
            url=self.base_url + '/todos/' + str(updated_todo.id),
            data=json.dumps(asdict(updated_todo)),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.text == ''

    def test_update_todo_with_missing_fields(self):
        """Обновление TODO с отсутствием обязательных полей"""
        original_todo = ToDo(id=2, text='Task to Update', completed=False)
        self.create_todo(original_todo)

        invalid_todo = {'id': 2, 'completed': True}

        response = self.http_session.put(
            url=self.base_url + '/todos/2',
            data=json.dumps(invalid_todo),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_update_todo_with_invalid_data_types(self):
        """Передача некорректных типов данных при обновлении"""
        original_todo = ToDo(id=3, text='Another Task', completed=False)
        self.create_todo(original_todo)

        invalid_todo = {'id': 3, 'text': 'Updated Task', 'completed': 'notBoolean'}

        response = self.http_session.put(
            url=self.base_url + '/todos/3',
            data=json.dumps(invalid_todo),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_update_todo_without_changing_data(self):
        """Обновление TODO без изменения данных"""
        original_todo = ToDo(id=4, text='Task without Changes', completed=False)
        self.create_todo(original_todo)

        response = self.http_session.put(
            url=self.base_url + '/todos/4',
            data=json.dumps(asdict(original_todo)),
            headers={'Content-Type': 'application/json'},
        )
        assert response.status_code == HTTPStatus.OK

        response = self.http_session.get(url=self.base_url + '/todos')
        assert response.status_code == HTTPStatus.OK
        body = response.json()

        assert body[0].get('text') == 'Task without Changes'
        assert body[0].get('completed') is False
