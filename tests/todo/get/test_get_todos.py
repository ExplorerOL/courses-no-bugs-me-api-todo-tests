import pytest

from src.models.todo import ToDo
from src.todo.requests.todo_request import ToDoRequest
from src.todo.requests.validated_todo_request import ValidatedToDoRequest
from tests.todo.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestGetTodos(BaseTest):
    def test_get_todo_when_database_is_empty(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Получение пустого списка TODO, когда база данных пуста"""
        todos = validated_todo_request_anonim.read_all()
        assert len(todos) == 0

    def test_get_todos_with_existing_entries(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Получение списка TODO с существующими записями"""
        todo1 = ToDo(id=1, text='Task 1', completed=False)
        todo2 = ToDo(id=2, text='Task 2', completed=True)

        validated_todo_request_anonim.create(data=todo1)
        validated_todo_request_anonim.create(data=todo2)

        todos = validated_todo_request_anonim.read_all()
        assert len(todos) == 2

        assert todos[0].id == 1
        assert todos[0].text == 'Task 1'
        assert todos[0].completed is False

        assert todos[1].id == 2
        assert todos[1].text == 'Task 2'
        assert todos[1].completed is True

    def test_get_todos_with_offset_and_limit(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Использование параметров offset и limit для пагинации"""
        for i in range(1, 6):
            validated_todo_request_anonim.create(data=ToDo(i, 'Task ' + str(i), bool(i % 2)))

        todos = validated_todo_request_anonim.read_all(limit=2, offset=2)

        assert todos[0].id == 3
        assert todos[0].text == 'Task 3'
        assert todos[1].id == 4
        assert todos[1].text == 'Task 4'

    def test_get_todos_with_invalid_offset_and_limit(self, todo_request_anonim: ToDoRequest):
        """Передача некорректных значений в offset и limit"""
        response = todo_request_anonim.read_all(limit=2, offset=-1)
        assert response.status_code == 400
        assert 'text/plain' in response.headers['Content-Type']
        assert response.text == 'Invalid query string'

    def test_get_todos_with_excessive_limit(self, validated_todo_request_anonim: ValidatedToDoRequest):
        """Проверка ответа при превышении максимально допустимого значения limit"""
        for i in range(1, 11):
            validated_todo_request_anonim.create(data=ToDo(i, 'Task ' + str(i), bool(i % 2)))

        todos = validated_todo_request_anonim.read_all(limit=1000, offset=0)
        assert len(todos) == 10

        # assert response.headers['Content-Type'] == 'application/json'
