import random

import pytest

from src.models.todo import ToDo
from src.support.generators.generators_todo import GeneratorsToDo
from src.todo.requests.validated_todo_request import ValidatedToDoRequest


@pytest.fixture(scope='function')
def delete_all_todos_scope_test(validated_todo_request_admin: ValidatedToDoRequest) -> None:
    todos = validated_todo_request_admin.read_all()
    for todo in todos:
        validated_todo_request_admin.delete(id=todo.id)


@pytest.fixture(scope='function')
def created_todo_with_random_data(validated_todo_request_admin: ValidatedToDoRequest) -> ToDo:
    todo = GeneratorsToDo.generate_todo_with_random_data()
    validated_todo_request_admin.create(data=todo)
    return todo


@pytest.fixture(scope='function')
def created_ten_or_more_todos_with_random_data(
    delete_all_todos_scope_test,
    validated_todo_request_admin: ValidatedToDoRequest,
) -> list[ToDo]:
    todos = [GeneratorsToDo.generate_todo_with_random_data() for _ in range(random.randint(10, 20))]
    for todo in todos:
        validated_todo_request_admin.create(data=todo)
    return todos
