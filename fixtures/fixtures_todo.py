import random

import pytest

from api.validated_todo_request import ValidatedToDoRequest
from models.todo import ToDo
from storages.tst_data_storage import TstDataStorage
from support.generators_todo import GeneratorsToDo


@pytest.fixture(scope='function')
def delete_all_todos_scope_test(validated_todo_request_admin: ValidatedToDoRequest) -> None:
    todos = validated_todo_request_admin.read_all()
    for todo in todos:
        validated_todo_request_admin.delete(id=todo.id)


@pytest.fixture(scope='session', autouse=True)
def delete_all_todos_after_testrun_scope_session(validated_todo_request_admin: ValidatedToDoRequest):
    yield
    for id in TstDataStorage().storage.keys():
        try:
            validated_todo_request_admin.delete(id=id)
        except AssertionError:
            pass


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


@pytest.fixture(scope='function')
def created_todos_with_random_data(
    delete_all_todos_scope_test,
    validated_todo_request_admin: ValidatedToDoRequest,
    request,
) -> list[ToDo]:
    quantity = getattr(request, 'param', 10)
    todos = [GeneratorsToDo.generate_todo_with_random_data() for _ in range(quantity)]
    [validated_todo_request_admin.create(data=todo) for todo in todos]
    return todos
