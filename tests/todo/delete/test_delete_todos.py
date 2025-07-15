from http import HTTPStatus

import pytest

from src.models.todo import ToDo
from src.todo.requests.validated_todo_request import ValidatedToDoRequest
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestDeleteTodos(BaseTest):
    def test_delete_existing_todo_with_valid_auth(self, validated_todo_request: ValidatedToDoRequest):
        """Успешное удаление существующего TODO с корректной авторизацией"""
        todo = ToDo(id=1, text='Task to Delete', completed=False)
        validated_todo_request.create(data=todo)

        body = validated_todo_request.delete(id=todo.id)

        assert body == ''
        todos = validated_todo_request.read_all()

        found = False
        for todo_item in todos:
            if todo_item.id == todo.id:
                found = True
                break
        assert not found, 'Удаленная задача все еще присутствует в списке TODO'

    def test_delete_todo_without_auth_header(self, validated_todo_request: ValidatedToDoRequest):
        """Попытка удаления TODO без заголовка Authorization"""
        todo = ToDo(id=2, text='Task to Delete', completed=False)
        self.create_todo(todo)

        response = self.http_session.delete(
            url=self.base_url + '/todos/' + str(todo.id),
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        response = self.http_session.get(url=self.base_url + '/todos')
        assert response.status_code == HTTPStatus.OK
        body = response.json()

        found = False
        for todo_item in body:
            if todo_item.get('id') == todo.id:
                found = True
                break
        assert found, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_todo_with_invalid_auth(self):
        """Попытка удаления TODO с некорректными учетными данными"""
        todo = ToDo(id=3, text='Task to Delete', completed=False)
        self.create_todo(todo)

        response = self.http_session.delete(
            url=self.base_url + '/todos/' + str(todo.id),
            auth=('invalidUser', 'invalidPass'),
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        response = self.http_session.get(url=self.base_url + '/todos')
        assert response.status_code == HTTPStatus.OK
        body = response.json()

        found = False
        for todo_item in body:
            if todo_item.get('id') == todo.id:
                found = True
                break
        assert found, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_non_existent_todo(self):
        """Удаление TODO с несуществующим id"""
        response = self.http_session.delete(
            url=self.base_url + '/todos/999',
            auth=('admin', 'admin'),
        )
        assert response.status_code == HTTPStatus.NOT_FOUND

        response = self.http_session.get(url=self.base_url + '/todos')
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        assert len(body) == 0

    def test_delete_todo_with_invalid_id_format(self):
        """Попытка удаления с некорректным форматом id"""
        response = self.http_session.delete(
            url=self.base_url + '/todos/invalidId',
            auth=('admin', 'admin'),
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
