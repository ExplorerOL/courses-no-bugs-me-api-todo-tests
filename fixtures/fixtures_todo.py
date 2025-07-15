import pytest

from src.todo.requests.validated_todo_request import ValidatedToDoRequest


@pytest.fixture(scope='function')
def delete_all_todos_scope_test(validated_todo_request_admin: ValidatedToDoRequest) -> None:
    todos = validated_todo_request_admin.read_all()
    for todo in todos:
        validated_todo_request_admin.delete(id=todo.id)
