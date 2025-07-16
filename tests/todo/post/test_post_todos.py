from http import HTTPStatus

import pytest

from src.models.todo import ToDo
from src.todo.requests.todo_request import ToDoRequest
from src.todo.requests.validated_todo_request import ValidatedToDoRequest
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestPostTodos(BaseTest):
    def test_create_todo_with_valid_data(self, validated_todo_request_anonim: ValidatedToDoRequest):
        new_todo = ToDo(id=1, text='New Task', completed=False)

        validated_todo_request_anonim.create(data=new_todo)

        actual_todos = validated_todo_request_anonim.read_all()

        found_todo = list(filter(lambda todo_item: todo_item.id == new_todo.id, actual_todos))
        assert found_todo, 'Созданная задача не найдена в списке TODO'

    def test_create_todo_with_max_length_text(self, validated_todo_request_anonim: ValidatedToDoRequest):
        max_length_text = ''.join('A' for i in range(255))
        new_todo = ToDo(id=3, text=max_length_text, completed=False)

        validated_todo_request_anonim.create(data=new_todo)

        actual_todos = validated_todo_request_anonim.read_all()

        found_todo = list(filter(lambda todo_item: todo_item.id == new_todo.id, actual_todos))
        assert found_todo, 'Созданная задача не найдена в списке TODO'

    def test_create_todo_with_existing_id(
        self,
        todo_request_anonim: ToDoRequest,
        validated_todo_request_anonim: ValidatedToDoRequest,
    ):
        first_todo = ToDo(id=5, text='First Task', completed=False)
        validated_todo_request_anonim.create(data=first_todo)

        duplicated_todo = ToDo(id=5, text='Duplicated Task', completed=True)

        response = todo_request_anonim.create(data=duplicated_todo)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.text == ''
