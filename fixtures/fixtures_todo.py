import random

import pytest

from api.todo_requester import ToDoRequester
from models.todo import ToDo
from storages.tst_data_storage import TstDataStorage
from support.generator_entities import GeneratorEntities


@pytest.fixture(scope='function')
def delete_all_todos_scope_test(todo_requester: ToDoRequester) -> None:
    todos = todo_requester.validated_todo_request_admin.read_all()
    for todo in todos:
        todo_requester.validated_todo_request_admin.delete(id=todo.id)


@pytest.fixture(scope='session', autouse=True)
def delete_all_todos_after_testrun_scope_session(todo_requester: ToDoRequester):
    yield
    for id in TstDataStorage().storage.keys():
        try:
            todo_requester.validated_todo_request_admin.delete(id=id)
        except AssertionError:
            pass


@pytest.fixture(scope='function')
def created_todo_with_random_data(todo_requester: ToDoRequester) -> ToDo:
    todo = GeneratorEntities.generate_entity_with_random_data(type=ToDo)
    todo_requester.validated_todo_request_admin.create(data=todo)
    return todo


@pytest.fixture(scope='function')
def created_ten_or_more_todos_with_random_data(
    delete_all_todos_scope_test,
    todo_requester: ToDoRequester,
) -> list[ToDo]:
    todos = [
        GeneratorEntities.generate_entity_with_random_data(type=ToDo) for _ in range(random.randint(10, 20))
    ]
    for todo in todos:
        todo_requester.validated_todo_request_admin.create(data=todo)
    return todos


@pytest.fixture(scope='function')
def created_todos_with_random_data(
    delete_all_todos_scope_test,
    todo_requester: ToDoRequester,
    request,
) -> list[ToDo]:
    quantity = getattr(request, 'param', 10)
    todos = [GeneratorEntities.generate_entity_with_random_data(type=ToDo) for _ in range(quantity)]
    [todo_requester.validated_todo_request_admin.create(data=todo) for todo in todos]
    return todos
