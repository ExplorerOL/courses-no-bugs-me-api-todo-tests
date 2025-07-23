from http import HTTPStatus

import pytest

from api.response_validators.api_response_validator import APIResponseValidator
from api.todo_requester import ToDoRequester
from models.todo import ToDo
from support.generators_string import GeneratorsString
from support.generators_todo import GeneratorsToDo
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestPostTodos(BaseTest):
    def test_create_todo_with_valid_data(self, todo_requester: ToDoRequester):
        # ARRANGE
        new_todo = GeneratorsToDo.generate_todo_with_random_data()
        # ACT
        todo_requester.validated_todo_request_anonim.create(data=new_todo)
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all()
        found_todo = list(filter(lambda todo_item: todo_item.id == new_todo.id, actual_todos))[0]
        assert found_todo, 'Созданная задача не найдена в списке TODO'
        assert found_todo == new_todo

    def test_create_todo_with_max_length_text(
        self,
        todo_requester: ToDoRequester,
    ):
        # ARRANGE
        new_todo = GeneratorsToDo.generate_todo_with_random_data()
        new_todo.text = GeneratorsString.generate_random_string(length=255)
        # ACT
        todo_requester.validated_todo_request_anonim.create(data=new_todo)
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all()
        found_todo = list(filter(lambda todo_item: todo_item.id == new_todo.id, actual_todos))[0]
        assert found_todo, 'Созданная задача не найдена в списке TODO'
        assert found_todo == new_todo

    def test_create_todo_with_existing_id(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        # ARRANGE
        duplicated_todo = GeneratorsToDo.generate_todo_with_random_data()
        duplicated_todo.id = created_todo_with_random_data.id
        response_validator = APIResponseValidator(
            expected_staus_code=HTTPStatus.BAD_REQUEST,
            expected_body='',
        )
        # ACT & ASSERT
        todo_requester.validated_todo_request_anonim.create(
            data=duplicated_todo,
            response_validator=response_validator,
        )
