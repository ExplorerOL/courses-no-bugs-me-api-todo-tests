import json

import pytest


@pytest.fixture(scope='function')
def delete_all_todos(self) -> None:
    todos_response = self.http_session.get(url=self.base_url + '/todos')
    todos = json.loads(todos_response.content)
    for todo in todos:
        self.http_session.delete(url=self.base_url + '/todos' + todo.id)
