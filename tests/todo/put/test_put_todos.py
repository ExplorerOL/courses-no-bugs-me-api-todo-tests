from http import HTTPStatus

import pytest

from api.response_validators.api_response_validator import APIResponseValidator
from api.validated_todo_request import ValidatedToDoRequest
from models.todo import ToDo
from support.generators_todo import GeneratorsToDo
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestPutTodos(BaseTest):
    def test_update_existing_todo_with_valid_data(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Обновление существующего TODO корректными данными"""
        # ARRANGE
        updated_todo = GeneratorsToDo.generate_todo_with_random_data()
        # ACT
        validated_todo_request_anonim.update(id=created_todo_with_random_data.id, data=updated_todo)
        # ASSERT
        actual_todos = validated_todo_request_anonim.read_all()
        assert len(actual_todos) == 1
        assert actual_todos[0] == updated_todo

    def test_update_non_existing_todo(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Попытка обновления TODO с несуществующим id"""
        # ARRANGE
        updated_todo = GeneratorsToDo.generate_todo_with_random_data()
        response_validator = APIResponseValidator(
            expected_staus_code=HTTPStatus.NOT_FOUND,
            expected_body='',
        )
        # ACT & ASSERT
        validated_todo_request_anonim.update(
            id=updated_todo.id, data=updated_todo, response_validator=response_validator
        )

    def test_update_todo_without_changing_data(
        self,
        validated_todo_request_anonim: ValidatedToDoRequest,
        created_todo_with_random_data: ToDo,
    ):
        """Обновление TODO без изменения данных"""
        # ACT
        validated_todo_request_anonim.update(
            id=created_todo_with_random_data.id,
            data=created_todo_with_random_data,
        )
        # ASSERT
        actual_todos = validated_todo_request_anonim.read_all()
        assert len(actual_todos) == 1
        assert actual_todos[0] == created_todo_with_random_data
