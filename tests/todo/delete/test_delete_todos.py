import random
from http import HTTPStatus

import pytest

from api.response_validators.api_response_validator import APIResponseValidator
from api.todo_requester import ToDoRequester
from api.validated_todo_request import ValidatedToDoRequest
from models.todo import ToDo
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_before_test_scope_test')
class TestDeleteTodos(BaseTest):
    def test_delete_existing_todo_with_valid_auth(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Успешное удаление существующего TODO с корректной авторизацией"""
        # ACT
        todo_requester.validated_todo_request_admin.delete(id=created_todo_with_random_data.id)
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_admin.read_all()
        found_todo = list(
            filter(lambda todo_item: todo_item.id == created_todo_with_random_data.id, actual_todos)
        )
        assert not found_todo, 'Удаленная задача все еще присутствует в списке TODO'

    def test_delete_todo_without_auth_header(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Попытка удаления TODO без заголовка Authorization"""
        # ARRANGE
        response_validator = APIResponseValidator(expected_staus_code=HTTPStatus.UNAUTHORIZED)
        # ACT
        todo_requester.validated_todo_request_anonim.delete(
            id=created_todo_with_random_data.id,
            response_validator=response_validator,
        )
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all()
        found_todo = list(
            filter(
                lambda todo_item: todo_item.id == created_todo_with_random_data.id,
                actual_todos,
            )
        )
        assert found_todo, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_todo_with_invalid_auth(
        self,
        todo_requester: ToDoRequester,
        validated_todo_request_wrong_auth: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Попытка удаления TODO с некорректными учетными данными"""
        # ARRANGE
        response_validator = APIResponseValidator(expected_staus_code=HTTPStatus.UNAUTHORIZED)
        # ACT
        validated_todo_request_wrong_auth.delete(
            id=created_todo_with_random_data.id,
            response_validator=response_validator,
        )
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all()
        found_todo = list(
            filter(
                lambda todo_item: todo_item.id == created_todo_with_random_data.id,
                actual_todos,
            )
        )
        assert found_todo, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    # TODO: обсудить, какой из вариантов лучше использовать
    def test_delete_non_existent_todo_var1(self, todo_requester: ToDoRequester):
        """Удаление TODO с несуществующим id"""
        # ARRANGE
        response_validator = APIResponseValidator(expected_staus_code=HTTPStatus.NOT_FOUND)
        # ACT
        todo_requester.validated_todo_request_admin.delete(
            id=random.randint(1, 1000),
            response_validator=response_validator,
        )
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_admin.read_all()
        assert len(actual_todos) == 0

    def test_delete_non_existent_todo_var2(self, todo_requester: ToDoRequester):
        """Удаление TODO с несуществующим id"""
        # ARRANGE
        response_validator = APIResponseValidator(expected_staus_code=HTTPStatus.NOT_FOUND)
        # ACT
        response = todo_requester.todo_request_admin.delete(id=random.randint(1, 1000))
        # ASSERT
        response_validator.validate_response(response=response)
        actual_todos = todo_requester.validated_todo_request_admin.read_all()
        assert len(actual_todos) == 0
