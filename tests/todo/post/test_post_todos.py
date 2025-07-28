import pytest

from api.response_validators.api_response_validators_templates import APIResponseValidatorsTemplates
from api.todo_requester import ToDoRequester
from models.todo import ToDo
from support.generators_string import GeneratorsString
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_before_test_scope_test')
class TestPostTodos(BaseTest):
    def test_create_todo_with_valid_data(
        self,
        todo_requester: ToDoRequester,
        todo_with_random_data_scope_test: ToDo,
    ):
        # ACT
        todo_requester.validated_todo_request_anonim.create(data=todo_with_random_data_scope_test)
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all()
        found_todo = list(
            filter(lambda todo_item: todo_item.id == todo_with_random_data_scope_test.id, actual_todos)
        )[0]
        assert found_todo, 'Созданная задача не найдена в списке TODO'
        assert found_todo == todo_with_random_data_scope_test

    def test_create_todo_with_max_length_text(
        self,
        todo_requester: ToDoRequester,
        todo_with_random_data_scope_test: ToDo,
    ):
        # ARRANGE
        todo_with_random_data_scope_test.text = GeneratorsString.generate_random_string(length=255)
        # ACT
        todo_requester.validated_todo_request_anonim.create(data=todo_with_random_data_scope_test)
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all()
        found_todo = list(
            filter(lambda todo_item: todo_item.id == todo_with_random_data_scope_test.id, actual_todos)
        )[0]
        assert found_todo, 'Созданная задача не найдена в списке TODO'
        assert found_todo == todo_with_random_data_scope_test

    def test_create_todo_with_existing_id(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
        todo_with_random_data_scope_test: ToDo,
    ):
        # ARRANGE
        duplicated_todo = todo_with_random_data_scope_test
        duplicated_todo.id = created_todo_with_random_data.id
        # ACT & ASSERT
        todo_requester.validated_todo_request_anonim.create(
            data=duplicated_todo,
            response_validator=APIResponseValidatorsTemplates.status_bad_req_body_empty,
        )
