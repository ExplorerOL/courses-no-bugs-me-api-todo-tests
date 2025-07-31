import random

import pytest

from api.response_validators.api_response_validators_templates import APIResponseValidatorsTemplates
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
        with self.ACT():
            with self.assert_soft:
                todo_requester.validated_todo_request_admin.delete(id=created_todo_with_random_data.id)
        with self.ASSERT():
            actual_todos = todo_requester.validated_todo_request_admin.read_all()
            found_todo = list(
                filter(lambda todo_item: todo_item.id == created_todo_with_random_data.id, actual_todos)
            )
            with self.assert_soft:
                assert not found_todo, 'Удаленная задача все еще присутствует в списке TODO'

    def test_delete_todo_without_auth_header(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Попытка удаления TODO без заголовка Authorization"""
        with self.ACT():
            with self.assert_soft:
                todo_requester.validated_todo_request_anonim.delete(
                    id=created_todo_with_random_data.id,
                    response_validator=APIResponseValidatorsTemplates.status_unauthorized,
                )
        with self.ASSERT():
            actual_todos = todo_requester.validated_todo_request_anonim.read_all()
            found_todo = list(
                filter(
                    lambda todo_item: todo_item.id == created_todo_with_random_data.id,
                    actual_todos,
                )
            )
            with self.assert_soft:
                assert found_todo, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_todo_with_invalid_auth(
        self,
        todo_requester: ToDoRequester,
        validated_todo_request_wrong_auth: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Попытка удаления TODO с некорректными учетными данными"""
        with self.ACT():
            with self.assert_soft:
                validated_todo_request_wrong_auth.delete(
                    id=created_todo_with_random_data.id,
                    response_validator=APIResponseValidatorsTemplates.status_unauthorized,
                )
        with self.ASSERT():
            actual_todos = todo_requester.validated_todo_request_anonim.read_all()
            found_todo = list(
                filter(
                    lambda todo_item: todo_item.id == created_todo_with_random_data.id,
                    actual_todos,
                )
            )
            with self.assert_soft:
                assert found_todo, 'Задача отсутствует в списке TODO, хотя не должна была быть удалена'

    def test_delete_non_existent_todo(self, todo_requester: ToDoRequester):
        """Удаление TODO с несуществующим id"""
        with self.ACT():
            with self.assert_soft:
                todo_requester.validated_todo_request_admin.delete(
                    id=random.randint(1, 1000),
                    response_validator=APIResponseValidatorsTemplates.status_not_found,
                )
        with self.ASSERT():
            actual_todos = todo_requester.validated_todo_request_admin.read_all()
            self.assertions.verify_is_equal(actual_value=len(actual_todos), expected_value=0)
