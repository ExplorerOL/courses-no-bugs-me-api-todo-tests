from config.config_general import config_general
from api.requests.todo_request import TodoRequest
from testrunner.base_test import BaseTest

class TestGetTodos(BaseTest):
    def test_get_todos_with_existing_entries(self):
        print(config_general.base_url)
        self.http_session.get()
