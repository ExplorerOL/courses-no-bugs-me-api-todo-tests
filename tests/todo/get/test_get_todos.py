from http import HTTPStatus
from itertools import zip_longest

import pytest

from api.todo_request import ToDoRequest
from api.validated_todo_request import ValidatedToDoRequest
from models.todo import ToDo
from support.decorators.decorator_prepare_todo import prepare_todos
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestGetTodos(BaseTest):
    def test_get_todo_when_database_is_empty(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Получение пустого списка TODO, когда база данных пуста"""
        # ACT
        todos = validated_todo_request_anonim.read_all()
        # ASSERT
        assert len(todos) == 0

    def test_get_todos_with_existing_entries(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_ten_or_more_todos_with_random_data: list[ToDo],
    ):
        """Получение списка TODO с существующими записями"""
        # ACT
        todos = validated_todo_request_anonim.read_all()
        # ASSERT
        for expected_todo, actual_todo in zip_longest(created_ten_or_more_todos_with_random_data, todos):
            assert expected_todo == actual_todo

    @pytest.mark.parametrize('created_todos_with_random_data', [20], indirect=True)
    @pytest.mark.parametrize('limit, offset', [(2, 2)])
    def test_get_todos_with_offset_and_limit(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_todos_with_random_data: list[ToDo],
        limit: int,
        offset: int,
    ):
        """Использование параметров offset и limit для пагинации"""
        # ACT
        actual_todos = validated_todo_request_anonim.read_all(limit=limit, offset=offset)
        # ASSERT
        assert len(actual_todos) == limit
        for i in range(limit):
            assert actual_todos[i] == created_todos_with_random_data[i + offset]

    @prepare_todos(quantity=20)
    @pytest.mark.parametrize('limit, offset', [(2, -1)])
    def test_get_todos_with_invalid_offset_and_limit(
        self, todo_request_anonim: ToDoRequest, limit: int, offset: int
    ):
        """Передача некорректных значений в offset и limit"""
        # ACT
        response = todo_request_anonim.read_all(limit=limit, offset=offset)
        # ASSERT
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert 'text/plain' in response.headers['Content-Type']
        assert response.text == 'Invalid query string'

    @pytest.mark.parametrize('created_todos_with_random_data', [20], indirect=True)
    def test_get_todos_with_excessive_limit(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_todos_with_random_data: list[ToDo],
    ):
        """Проверка ответа при превышении максимально допустимого значения limit"""
        # ACT
        todos = validated_todo_request_anonim.read_all(limit=1000, offset=0)
        # ASSERT
        assert len(todos) == len(created_todos_with_random_data)
