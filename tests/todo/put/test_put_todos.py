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
            EXPETED_TODO_COUNT = 1
            updated_todo = GeneratorsEntity.generate_entity_with_random_data(entity_type=ToDo)
        with self.ACT():
            todo_requester.validated_todo_request_anonim.update(
                id=created_todo_with_random_data.id,
                data=updated_todo,
                soft_validation=True,
            )
        with self.ASSERT(msg='Проверка количества TODO'):
            actual_todos = todo_requester.validated_todo_request_anonim.read_all()
            self.assertions.verify_is_equal(
                actual_value=len(actual_todos),
                expected_value=EXPETED_TODO_COUNT,
            )
        with self.ASSERT(msg='Проверка данных TODO'):
            self.assertions.verify_is_equal(
                actual_value=actual_todos[0],
                expected_value=updated_todo,
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
            EXPETED_TODO_COUNT = 1
        with self.ACT():
            todo_requester.validated_todo_request_anonim.update(
                id=created_todo_with_random_data.id,
                data=created_todo_with_random_data,
                soft_validation=True,
            )
        with self.ASSERT(msg='Проверка количества TODO'):
            actual_todos = todo_requester.validated_todo_request_anonim.read_all()
            self.assertions.verify_is_equal(
                actual_value=len(actual_todos),
                expected_value=EXPETED_TODO_COUNT,
            )
        with self.ASSERT(msg='Проверка данных TODO'):
            self.assertions.verify_is_equal(
                actual_value=actual_todos[0],
                expected_value=created_todo_with_random_data,
            )
