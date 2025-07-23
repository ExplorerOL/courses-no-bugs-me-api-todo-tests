from http import HTTPStatus

import pytest

from api.response_validators.api_response_validator import APIResponseValidator
from api.todo_requester import ToDoRequester
from managers.manager_todo import manager_todo
from models.todo import ToDo
from support.generator_entities import GeneratorEntities
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_before_test_scope_test')
class TestPutTodos(BaseTest):
    def test_update_existing_todo_with_valid_data(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Обновление существующего TODO корректными данными"""
        # ARRANGE
        updated_todo = GeneratorEntities.generate_entity_with_random_data(type=ToDo)
        # ACT
        todo_requester.validated_todo_request_anonim.update(
            id=created_todo_with_random_data.id,
            data=updated_todo,
        )
        manager_todo.add_data(data=updated_todo)
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all()
        assert len(actual_todos) == 1
        assert actual_todos[0] == updated_todo

    def test_update_non_existing_todo(self, todo_requester: ToDoRequester):
        """Попытка обновления TODO с несуществующим id"""
        # ARRANGE
        updated_todo = GeneratorEntities.generate_entity_with_random_data(type=ToDo)
        response_validator = APIResponseValidator(
            expected_staus_code=HTTPStatus.NOT_FOUND,
            expected_body='',
        )
        # ACT & ASSERT
        todo_requester.validated_todo_request_anonim.update(
            id=updated_todo.id,
            data=updated_todo,
            response_validator=response_validator,
        )

    def test_update_todo_without_changing_data(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Обновление TODO без изменения данных"""
        # ACT
        todo_requester.validated_todo_request_anonim.update(
            id=created_todo_with_random_data.id,
            data=created_todo_with_random_data,
        )
        # ASSERT
        actual_todos = todo_requester.validated_todo_request_anonim.read_all()
        assert len(actual_todos) == 1
        assert actual_todos[0] == created_todo_with_random_data
