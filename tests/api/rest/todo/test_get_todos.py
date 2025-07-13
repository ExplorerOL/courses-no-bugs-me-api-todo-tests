import pytest

# from api.requests.todo_request import TodoRequest
from config.endpoints import Endpoints
from testrunner.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos')
class TestGetTodos(BaseTest):
    def test_get_todos_with_existing_entries(self):
        """Получение пустого списка TODO при пустой БД"""
        response = self.http_session.get(url=self.base_url + Endpoints.todos)

        assert response.status_code == 200
        body = response.json()
        assert len(body) == 0
