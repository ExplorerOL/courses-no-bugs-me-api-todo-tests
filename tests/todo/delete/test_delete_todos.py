from http import HTTPStatus

import pytest

from src.models.todo import ToDo
from src.todo.requests.todo_request import ToDoRequest
from src.todo.requests.validated_todo_request import ValidatedToDoRequest
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestDeleteTodos(BaseTest):
    def test_delete_existing_todo_with_valid_auth(self, validated_todo_request_admin: ValidatedToDoRequest):
        """Успешное удаление существующего TODO с корректной авторизацией"""
        todo = ToDo(id=1, text='Task to Delete', completed=False)
        validated_todo_request_admin.create(data=todo)

        body = validated_todo_request_admin.delete(id=todo.id)

        assert body == ''
        actual_todos = validated_todo_request_admin.read_all()

        found_todo = list(filter(lambda todo_item: todo_item.id == todo.id, actual_todos))
        assert not found_todo, 'Удаленная задача все еще присутствует в списке TODO'

    def test_delete_todo_without_auth_header(
        self,
        todo_request_anonim: ToDoRequest,
        validated_todo_request_anonim: ValidatedToDoRequest,
    ):
        """Попытка удаления TODO без заголовка Authorization"""
        todo = ToDo(id=2, text='Task to Delete', completed=False)
        validated_todo_request_anonim.create(data=todo)

        response = todo_request_anonim.delete(id=todo.id)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        actual_todos = validated_todo_request_anonim.read_all()

        found_todo = list(filter(lambda todo_item: todo_item.id == todo.id, actual_todos))
        assert found_todo, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_todo_with_invalid_auth(
        self,
        todo_request_wrong_auth: ToDoRequest,
        validated_todo_request_anonim: ValidatedToDoRequest,
    ):
        """Попытка удаления TODO с некорректными учетными данными"""
        todo = ToDo(id=3, text='Task to Delete', completed=False)
        validated_todo_request_anonim.create(data=todo)

        response = todo_request_wrong_auth.delete(id=todo.id)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        actual_todos = validated_todo_request_anonim.read_all()

        found_todo = list(filter(lambda todo_item: todo_item.id == todo.id, actual_todos))
        assert found_todo, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_non_existent_todo(
        self,
        todo_request_admin: ToDoRequest,
        validated_todo_request_anonim: ValidatedToDoRequest,
    ):
        """Удаление TODO с несуществующим id"""
        response = todo_request_admin.delete(id=999)
        assert response.status_code == HTTPStatus.NOT_FOUND

        actual_todos = validated_todo_request_anonim.read_all()
        assert len(actual_todos) == 0
