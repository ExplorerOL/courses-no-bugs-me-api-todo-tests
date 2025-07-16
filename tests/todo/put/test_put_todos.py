from http import HTTPStatus

import pytest

from src.models.todo import ToDo
from src.todo.requests.todo_request import ToDoRequest
from src.todo.requests.validated_todo_request import ValidatedToDoRequest
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestPutTodos(BaseTest):
    def test_update_existing_todo_with_valid_data(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Обновление существующего TODO корректными данными"""
        original_todo = ToDo(id=1, text='Original Task', completed=False)
        validated_todo_request_anonim.create(data=original_todo)

        updated_todo = ToDo(id=1, text='Updated Task', completed=True)
        validated_todo_request_anonim.update(id=original_todo.id, data=updated_todo)

        actual_todos = validated_todo_request_anonim.read_all()

        assert len(actual_todos) == 1
        assert actual_todos[0].text == 'Updated Task'
        assert actual_todos[0].completed is True

    def test_update_non_existing_todo(self, todo_request_anonim: ToDoRequest):
        """Попытка обновления TODO с несуществующим id"""
        updated_todo = ToDo(id=999, text='Non-existent Task', completed=True)

        response = todo_request_anonim.update(id=999, data=updated_todo)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.text == ''

    def test_update_todo_without_changing_data(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Обновление TODO без изменения данных"""
        original_todo = ToDo(id=4, text='Task without Changes', completed=False)
        validated_todo_request_anonim.create(data=original_todo)

        actual_todos = validated_todo_request_anonim.read_all()

        assert actual_todos[0].text == 'Task without Changes'
        assert actual_todos[0].completed is False
