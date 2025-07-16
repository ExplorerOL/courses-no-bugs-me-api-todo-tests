import random
from http import HTTPStatus

import pytest

from src.models.todo import ToDo
from src.todo.requests.todo_request import ToDoRequest
from src.todo.requests.validated_todo_request import ValidatedToDoRequest
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestDeleteTodos(BaseTest):
    def test_delete_existing_todo_with_valid_auth(
        self,
        validated_todo_request_admin: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Успешное удаление существующего TODO с корректной авторизацией"""
        # ACT
        validated_todo_request_admin.delete(id=created_todo_with_random_data.id)
        # ASSERT
        actual_todos = validated_todo_request_admin.read_all()
        found_todo = list(
            filter(lambda todo_item: todo_item.id == created_todo_with_random_data.id, actual_todos)
        )
        assert not found_todo, 'Удаленная задача все еще присутствует в списке TODO'

    def test_delete_todo_without_auth_header(
        self,
        todo_request_anonim: ToDoRequest,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Попытка удаления TODO без заголовка Authorization"""
        # ACT
        response = todo_request_anonim.delete(id=created_todo_with_random_data.id)
        # ASSERT
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        actual_todos = validated_todo_request_anonim.read_all()
        found_todo = list(
            filter(
                lambda todo_item: todo_item.id == created_todo_with_random_data.id,
                actual_todos,
            )
        )
        assert found_todo, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_todo_with_invalid_auth(
        self,
        todo_request_wrong_auth: ToDoRequest,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Попытка удаления TODO с некорректными учетными данными"""
        # ACT
        response = todo_request_wrong_auth.delete(id=created_todo_with_random_data.id)
        # ASSERT
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        actual_todos = validated_todo_request_anonim.read_all()
        found_todo = list(
            filter(
                lambda todo_item: todo_item.id == created_todo_with_random_data.id,
                actual_todos,
            )
        )
        assert found_todo, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_non_existent_todo(
        self,
        todo_request_admin: ToDoRequest,
        validated_todo_request_anonim: ValidatedToDoRequest,
    ):
        """Удаление TODO с несуществующим id"""
        # ACT
        response = todo_request_admin.delete(id=random.randint(1, 1000))
        # ASSERT
        assert response.status_code == HTTPStatus.NOT_FOUND
        actual_todos = validated_todo_request_anonim.read_all()
        assert len(actual_todos) == 0
