import pytest

from api.rest.models.models import ToDo
from config.endpoints import Endpoints
from testrunner.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos_scope_test')
class TestGetTodos(BaseTest):
    def test_get_todo_when_database_is_empty(self):
        """Получение пустого списка TODO, когда база данных пуста"""
        response = self.http_session.get(url=self.base_url + Endpoints.todos)

        assert response.status_code == 200
        body = response.json()
        assert len(body) == 0

    def test_get_todos_with_existing_entries(self):
        """Получение списка TODO с существующими записями"""
        todo1 = ToDo(id=1, text='Task 1', completed=False)
        todo2 = ToDo(id=2, text='Task 2', completed=True)

        self.create_todo(todo1)
        self.create_todo(todo2)

        response = self.http_session.get(url=self.base_url + Endpoints.todos)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        body = response.json()
        assert len(body) == 2

        assert body[0].get('id') == 1
        assert body[0].get('text') == 'Task 1'
        assert body[0].get('completed') is False

        assert body[1].get('id') == 2
        assert body[1].get('text') == 'Task 2'
        assert body[1].get('completed') is True

    def test_get_todos_with_offset_and_limit(self):
        """Использование параметров offset и limit для пагинации"""
        for i in range(1, 6):
            self.create_todo(ToDo(i, 'Task ' + str(i), bool(i % 2)))

        response = self.http_session.get(
            url=self.base_url + Endpoints.todos, params={'limit': 2, 'offset': 2}
        )
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        body = response.json()

        assert body[0].get('id') == 3
        assert body[0].get('text') == 'Task 3'

        assert body[1].get('id') == 4
        assert body[1].get('text') == 'Task 4'

    def test_get_todos_with_invalid_offset_and_limit(self):
        """Передача некорректных значений в offset и limit"""

    def test_get_todos_with_excessive_limit(self):
        """Проверка ответа при превышении максимально допустимого значения limit"""
        for i in range(1, 11):
            self.create_todo(ToDo(i, 'Task ' + str(i), bool(i % 2)))

        response = self.http_session.get(url=self.base_url + Endpoints.todos, params={'limit': 1000})
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        body = response.json()
        todos = [ToDo(**todo) for todo in body]
        print(todos)
        assert len(todos) == 10
