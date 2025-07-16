from http import HTTPStatus

import pytest

from src.models.todo import ToDo
from src.support.generators.generators_todo import GeneratorsToDo
from src.todo.requests.todo_request import ToDoRequest
from src.todo.requests.validated_todo_request import ValidatedToDoRequest
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestPutTodos(BaseTest):
    def test_update_existing_todo_with_valid_data(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Обновление существующего TODO корректными данными"""
        # ARRANGE
        updated_todo = GeneratorsToDo.generate_todo_with_random_data()
        # ACT
        validated_todo_request_anonim.update(id=created_todo_with_random_data.id, data=updated_todo)
        # ASSERT
        actual_todos = validated_todo_request_anonim.read_all()
        assert len(actual_todos) == 1
        assert actual_todos[0].id == updated_todo.id
        assert actual_todos[0].text == updated_todo.text
        assert actual_todos[0].completed == updated_todo.completed

    def test_update_non_existing_todo(self, todo_request_anonim: ToDoRequest):
        """Попытка обновления TODO с несуществующим id"""
        # ARRANGE
        updated_todo = GeneratorsToDo.generate_todo_with_random_data()
        # ACT
        response = todo_request_anonim.update(id=updated_todo.id, data=updated_todo)
        # ASSERT
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.text == ''

    def test_update_todo_without_changing_data(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Обновление TODO без изменения данных"""
        # ACT
        validated_todo_request_anonim.update(
            id=created_todo_with_random_data.id,
            data=created_todo_with_random_data,
        )
        # ASSERT
        actual_todos = validated_todo_request_anonim.read_all()
        assert actual_todos[0].id == created_todo_with_random_data.id
        assert actual_todos[0].text == created_todo_with_random_data.text
        assert actual_todos[0].completed == created_todo_with_random_data.completed
