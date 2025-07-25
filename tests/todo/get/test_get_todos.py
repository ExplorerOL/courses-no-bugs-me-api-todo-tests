from http import HTTPStatus
from itertools import zip_longest

import pytest

from api.response_validators.api_response_validator import APIResponseValidator
from api.todo_requester import ToDoRequester
from models.todo import ToDo
from support.decorators.decorator_mobile import mobile  # noqa
from support.decorators.decorator_prepare_todo import prepare_todos
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_before_test_scope_test')
class TestGetTodos(BaseTest):
    def test_get_todo_when_database_is_empty(self, todo_requester: ToDoRequester):
        """Получение пустого списка TODO, когда база данных пуста"""
        # ACT
        todos = todo_requester.validated_todo_request_anonim.read_all()
        # ASSERT
        assert len(todos) == 0

    def test_get_todos_with_existing_entries(
        self,
        todo_requester: ToDoRequester,
        created_ten_or_more_todos_with_random_data: list[ToDo],
    ):
        """Получение списка TODO с существующими записями"""
        # ACT
        todos = todo_requester.validated_todo_request_anonim.read_all()
        # ASSERT
        for expected_todo, actual_todo in zip_longest(created_ten_or_more_todos_with_random_data, todos):
            assert expected_todo == actual_todo

    @pytest.mark.parametrize('created_todos_with_random_data', [20], indirect=True)
    @pytest.mark.parametrize('limit, offset', [(2, 2)])
    def test_get_todos_with_offset_and_limit(
        self,
        todo_requester: ToDoRequester,
        created_todos_with_random_data: list[ToDo],
        limit: int,
        offset: int,
    ):
        """Использование параметров offset и limit для пагинации"""
        # ACT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all(limit=limit, offset=offset)
        # ASSERT
        assert len(actual_todos) == limit
        for i in range(limit):
            assert actual_todos[i] == created_todos_with_random_data[i + offset]

    # @mobile
    @prepare_todos(quantity=20)
    @pytest.mark.parametrize('limit, offset', [(2, -1)])
    def test_get_todos_with_invalid_offset_and_limit(
        self,
        todo_requester: ToDoRequester,
        limit: int,
        offset: int,
    ):
        """Передача некорректных значений в offset и limit"""
        # ARRANGE
        response_validator = APIResponseValidator(
            expected_staus_code=HTTPStatus.BAD_REQUEST,
            expected_headers={'Content-Type': 'text/plain; charset=utf-8'},
            expected_body='Invalid query string',
        )
        # ACT & ASSERT
        todo_requester.validated_todo_request_anonim.read_all(
            limit=limit,
            offset=offset,
            response_validator=response_validator,
        )

    @pytest.mark.parametrize('created_todos_with_random_data', [20], indirect=True)
    def test_get_todos_with_excessive_limit(
        self,
        todo_requester: ToDoRequester,
        created_todos_with_random_data: list[ToDo],
    ):
        """Проверка ответа при превышении максимально допустимого значения limit"""
        # ACT
        todos = todo_requester.validated_todo_request_anonim.read_all(limit=1000, offset=0)
        # ASSERT
        assert len(todos) == len(created_todos_with_random_data)
