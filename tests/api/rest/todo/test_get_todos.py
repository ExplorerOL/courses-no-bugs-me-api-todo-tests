import pytest
from config.config_general import config_general

# from api.requests.todo_request import TodoRequest
from testrunner.base_test import BaseTest


@pytest.mark.usefixtures('delete_all_todos')
class TestGetTodos(BaseTest):
    def test_get_todos_with_existing_entries(self):
        print(config_general.base_url)
        response = self.http_session.get(url=self.base_url + '/todos')
        print(response.json())
