import pytest

from api.response_validators.api_response_validators_templates import APIResponseValidatorsTemplates
from api.todo_requester import ToDoRequester
from models.todo import ToDo
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_before_test_scope_test')
class TestDeleteTodos(BaseTest):
    def test_delete_todo(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Удаление TODO"""
        with self.ARRANGE():
            EXPECTED_TODOS_COUNT = 0
        with self.ACT():
            todo_requester.validated_todo_request_admin.delete(
                id=created_todo_with_random_data.id,
                soft_validation=True,
            )
        with self.ASSERT():
            todo_requester.validated_todo_request_admin.verify_todos_count(
                expected_count=EXPECTED_TODOS_COUNT
            )

    def test_delete_todo_by_not_authorized_user(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Удаление TODO неавторизованным пользователем"""
        with self.ARRANGE():
            EXPECTED_TODOS_COUNT = 1
        with self.ACT():
            todo_requester.validated_todo_request_anonim.delete(
                id=created_todo_with_random_data.id,
                response_validator=APIResponseValidatorsTemplates.status_unauthorized,
                soft_validation=True,
            )
        with self.ASSERT():
            todo_requester.validated_todo_request_admin.verify_todos_count(
                expected_count=EXPECTED_TODOS_COUNT
            )

    def test_delete_not_existing_todo(
        self,
        todo_requester: ToDoRequester,
        created_ten_or_more_todos_with_random_data: list[ToDo],
        actual_todos_max_id: int,
    ):
        """Удаление TODO с несуществующим id"""
        with self.ARRANGE():
            expected_todos_count = len(created_ten_or_more_todos_with_random_data)
            not_existing_id = actual_todos_max_id + 1
        with self.ACT():
            todo_requester.validated_todo_request_admin.delete(
                id=not_existing_id,
                response_validator=APIResponseValidatorsTemplates.status_not_found,
                soft_validation=True,
            )
        with self.ASSERT():
            todo_requester.validated_todo_request_admin.verify_todos_count(
                expected_count=expected_todos_count
            )
