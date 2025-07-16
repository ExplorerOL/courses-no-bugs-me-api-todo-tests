from itertools import zip_longest

import pytest

from src.models.todo import ToDo
from src.todo.requests.todo_request import ToDoRequest
from src.todo.requests.validated_todo_request import ValidatedToDoRequest
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestGetTodos(BaseTest):
    def test_get_todo_when_database_is_empty(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Получение пустого списка TODO, когда база данных пуста"""
        todos = validated_todo_request_anonim.read_all()
        assert len(todos) == 0

    def test_get_todos_with_existing_entries(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_ten_or_more_todos_with_random_data: list[ToDo],
    ):
        """Получение списка TODO с существующими записями"""
        todos = validated_todo_request_anonim.read_all()

        for expected_todo, actual_todo in zip_longest(created_ten_or_more_todos_with_random_data, todos):
            assert expected_todo.id == actual_todo.id
            assert expected_todo.text == actual_todo.text
            assert expected_todo.completed == actual_todo.completed

    def test_get_todos_with_offset_and_limit(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_ten_or_more_todos_with_random_data: list[ToDo],
    ):
        """Использование параметров offset и limit для пагинации"""
        limit = 2
        offset = 2

        actual_todos = validated_todo_request_anonim.read_all(limit=limit, offset=offset)

        assert len(actual_todos) == limit
        for i in range(limit):
            assert actual_todos[i].id == created_ten_or_more_todos_with_random_data[i + offset].id
            assert actual_todos[i].text == created_ten_or_more_todos_with_random_data[i + offset].text

    def test_get_todos_with_invalid_offset_and_limit(self, todo_request_anonim: ToDoRequest):
        """Передача некорректных значений в offset и limit"""
        response = todo_request_anonim.read_all(limit=2, offset=-1)
        assert response.status_code == 400
        assert 'text/plain' in response.headers['Content-Type']
        assert response.text == 'Invalid query string'

    def test_get_todos_with_excessive_limit(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_ten_or_more_todos_with_random_data: list[ToDo],
    ):
        """Проверка ответа при превышении максимально допустимого значения limit"""

        todos = validated_todo_request_anonim.read_all(limit=1000, offset=0)
        assert len(todos) == len(created_ten_or_more_todos_with_random_data)
