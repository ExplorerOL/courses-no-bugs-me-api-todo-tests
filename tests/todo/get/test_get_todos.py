import pytest

from api.response_validators.api_response_validators_templates import APIResponseValidatorsTemplates
from api.todo_requester import ToDoRequester
from models.todo import ToDo
from support.decorators.decorator_prepare_todo import prepare_todos
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_before_test_scope_test')
class TestGetTodos(BaseTest):
    def test_get_todo_when_database_is_empty(self, todo_requester: ToDoRequester):
        """Получение пустого списка TODO, когда база данных пуста"""
        with self.ARRANGE():
            EXPETED_TODO_COUNT = 0
        with self.ACT():
            todos = todo_requester.validated_todo_request_anonim.read_all(soft_validation=True)
        with self.ASSERT(msg='Проверка количества TODO'):
            self.assertions.verify_is_equal(
                actual_value=len(todos),
                expected_value=EXPETED_TODO_COUNT,
            )

    def test_get_todos_with_existing_entries(
        self,
        todo_requester: ToDoRequester,
        created_ten_or_more_todos_with_random_data: list[ToDo],
    ):
        """Получение списка TODO с существующими записями"""
        with self.ACT():
            todos = todo_requester.validated_todo_request_anonim.read_all(soft_validation=True)
        with self.ASSERT(msg='Проверка количества TODO'):
            self.assertions.verify_is_equal(
                actual_value=len(todos),
                expected_value=len(created_ten_or_more_todos_with_random_data),
            )

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
        with self.ACT():
            actual_todos = todo_requester.validated_todo_request_anonim.read_all(
                limit=limit,
                offset=offset,
                soft_validation=True,
            )
        with self.ASSERT(msg='Проверка количества TODO'):
            self.assertions.verify_is_equal(
                actual_value=len(actual_todos),
                expected_value=limit,
            )

    # Декоратор закомментирован, так как тестовое приложение не поддерживает эдпоинты /mobile
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
        with self.ACT():
            todo_requester.validated_todo_request_anonim.read_all(
                limit=limit,
                offset=offset,
                response_validator=APIResponseValidatorsTemplates.status_bad_req_body_invalid_query_string,
                soft_validation=True,
            )

    @pytest.mark.parametrize('created_todos_with_random_data', [20], indirect=True)
    def test_get_todos_with_excessive_limit(
        self,
        todo_requester: ToDoRequester,
        created_todos_with_random_data: list[ToDo],
    ):
        """Проверка ответа при превышении максимально допустимого значения limit"""
        with self.ARRANGE():
            LIMIT = 1000
            OFFSET = 0
        with self.ACT():
            todos = todo_requester.validated_todo_request_anonim.read_all(
                limit=LIMIT,
                offset=OFFSET,
                soft_validation=True,
            )
        with self.ASSERT(msg='Проверка количества TODO'):
            self.assertions.verify_is_equal(
                actual_value=len(todos),
                expected_value=len(created_todos_with_random_data),
            )
