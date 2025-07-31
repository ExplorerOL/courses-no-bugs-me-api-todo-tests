import pytest

from api.response_validators.api_response_validators_templates import APIResponseValidatorsTemplates
from api.todo_requester import ToDoRequester
from models.todo import ToDo
from support.generators.generators_string import GeneratorsString
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_before_test_scope_test')
class TestPostTodos(BaseTest):
    def test_create_todo_with_valid_data(
        self,
        todo_requester: ToDoRequester,
        todo_with_random_data_scope_test: ToDo,
    ):
        with self.ACT():
            with self.assert_soft:
                todo_requester.validated_todo_request_anonim.create(data=todo_with_random_data_scope_test)
        with self.ASSERT():
            actual_todo = todo_requester.validated_todo_request_anonim.read_all()[0]
            self.assertions.verify_is_equal(
                actual_value=actual_todo,
                expected_value=todo_with_random_data_scope_test,
                msg='Проверка данных TODO',
            )

    def test_create_todo_with_max_length_text(
        self,
        todo_requester: ToDoRequester,
        todo_with_random_data_scope_test: ToDo,
    ):
        with self.ARRANGE():
            todo_with_random_data_scope_test.text = GeneratorsString.generate_random_string(length=255)
        with self.ACT():
            with self.assert_soft:
                todo_requester.validated_todo_request_anonim.create(data=todo_with_random_data_scope_test)
        with self.ASSERT():
            actual_todo = todo_requester.validated_todo_request_anonim.read_all()[0]
            self.assertions.verify_is_equal(
                actual_value=actual_todo,
                expected_value=todo_with_random_data_scope_test,
                msg='Проверка данных TODO',
            )

    def test_create_todo_with_existing_id(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
        todo_with_random_data_scope_test: ToDo,
    ):
        with self.ARRANGE():
            duplicated_todo = todo_with_random_data_scope_test
            duplicated_todo.id = created_todo_with_random_data.id
        with self.ACT():
            with self.assert_soft:
                todo_requester.validated_todo_request_anonim.create(
                    data=duplicated_todo,
                    response_validator=APIResponseValidatorsTemplates.status_bad_req_body_empty,
                )
