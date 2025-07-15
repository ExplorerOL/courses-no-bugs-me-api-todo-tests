import pytest

from src.todo.requests.validated_todo_request import ValidatedToDoRequest


@pytest.fixture(scope='function')
def delete_all_todos_scope_test(validated_todo_request: ValidatedToDoRequest) -> None:
    todos = validated_todo_request.read_all()
    for todo in todos:
        validated_todo_request.delete(id=todo.id)
