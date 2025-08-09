import pytest

from api.response_validators.api_response_validators_templates import APIResponseValidatorsTemplates
from api.todo_requester import ToDoRequester
from fixtures.fixtures_notifications import delete_all_notifications_before_test_scope_test  # noqa
from models.todo import ToDo
from support.generators.generators_string import GeneratorsString
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures(
    'delete_all_todos_before_test_scope_test',
    'delete_all_notifications_before_test_scope_test',
)
class TestPostTodos(BaseTest):
    def test_create_todo(
        self,
        todo_requester: ToDoRequester,
        todo_with_random_data_scope_test: ToDo,
    ):
        """Создание TODO"""
        todo_requester.validated_todo_notification_anonim.read_all()
        with self.ACT():
            todo_requester.validated_todo_request_anonim.create(
                data=todo_with_random_data_scope_test,
                soft_validation=True,
            )
        with self.ASSERT():
            todo_requester.validated_todo_request_anonim.verify_todo_data(
                expected_data=todo_with_random_data_scope_test,
            )
            todo_requester.validated_todo_notification_anonim.verify_notification_data(
                expected_data=todo_with_random_data_scope_test
            )

    def test_create_todo_with_max_text_length(
        self,
        todo_requester: ToDoRequester,
        todo_with_random_data_scope_test: ToDo,
    ):
        """Создание TODO с максимальной длиной текста"""
        with self.ARRANGE():
            MAX_TEXT_LENGTH = 255
            todo_with_random_data_scope_test.text = GeneratorsString.generate_random_string(
                length=MAX_TEXT_LENGTH
            )
        with self.ACT():
            todo_requester.validated_todo_request_anonim.create(
                data=todo_with_random_data_scope_test,
                soft_validation=True,
            )
        with self.ASSERT():
            todo_requester.validated_todo_request_anonim.verify_todo_data(
                expected_data=todo_with_random_data_scope_test,
            )
            todo_requester.validated_todo_notification_anonim.verify_notification_data(
                expected_data=todo_with_random_data_scope_test
            )

    def test_create_todo_with_existing_id(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
        todo_with_random_data_scope_test: ToDo,
    ):
        """Создание TODO с существующим id"""
        with self.ARRANGE():
            duplicated_todo = todo_with_random_data_scope_test
            duplicated_todo.id = created_todo_with_random_data.id
        with self.ACT():
            todo_requester.validated_todo_request_anonim.create(
                data=duplicated_todo,
                response_validator=APIResponseValidatorsTemplates.status_bad_req_body_empty,
                soft_validation=True,
            )
            todo_requester.validated_todo_notification_anonim.verify_no_notifications_present()
