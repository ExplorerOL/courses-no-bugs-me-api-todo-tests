import pytest

from api.response_validators.api_response_validators_templates import APIResponseValidatorsTemplates
from api.todo_requester import ToDoRequester
from models.todo import ToDo
from support.generators.generators_entity import GeneratorsEntity
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_before_test_scope_test')
class TestPutTodos(BaseTest):
    def test_update_existing_todo_with_valid_data(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Обновление существующего TODO корректными данными"""
        with self.ARRANGE():
            EXPECTED_TODOS_COUNT = 1
            updated_todo = GeneratorsEntity.generate_entity_with_random_data(entity_type=ToDo)
        with self.ACT():
            todo_requester.validated_todo_request_anonim.update(
                id=created_todo_with_random_data.id,
                data=updated_todo,
                soft_validation=True,
            )
        with self.ASSERT():
            todo_requester.validated_todo_request_admin.verify_todos_count(
                expected_count=EXPECTED_TODOS_COUNT
            )
            todo_requester.validated_todo_request_admin.verify_todo_data(
                todo_id=updated_todo.id, expected_data=updated_todo
            )

    def test_update_non_existing_todo(self, todo_requester: ToDoRequester):
        """Попытка обновления TODO с несуществующим id"""
        with self.ARRANGE():
            updated_todo = GeneratorsEntity.generate_entity_with_random_data(entity_type=ToDo)
        with self.ACT():
            todo_requester.validated_todo_request_anonim.update(
                id=updated_todo.id,
                data=updated_todo,
                response_validator=APIResponseValidatorsTemplates.status_not_found_body_empty,
                soft_validation=True,
            )

    def test_update_todo_without_changing_data(
        self,
        todo_requester: ToDoRequester,
        created_todo_with_random_data: ToDo,
    ):
        """Обновление TODO без изменения данных"""
        with self.ARRANGE():
            EXPECTED_TODOS_COUNT = 1
        with self.ACT():
            todo_requester.validated_todo_request_anonim.update(
                id=created_todo_with_random_data.id,
                data=created_todo_with_random_data,
                soft_validation=True,
            )
        with self.ASSERT():
            todo_requester.validated_todo_request_admin.verify_todos_count(
                expected_count=EXPECTED_TODOS_COUNT
            )
            todo_requester.validated_todo_request_admin.verify_todo_data(
                todo_id=created_todo_with_random_data.id,
                expected_data=created_todo_with_random_data,
            )
