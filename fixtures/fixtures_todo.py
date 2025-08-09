import random

import pytest

from api.todo_requester import ToDoRequester
from fixtures.fixtures_general import test_app_before_testrun  # noqa
from managers.manager_todo import manager_todo
from models.todo import ToDo
from support.generators.generators_entity import GeneratorsEntity


@pytest.fixture(scope='function')
def delete_all_todos_before_test_scope_test() -> None:
    manager_todo.delete_all_entities()


@pytest.fixture(scope='session', autouse=True)
def delete_all_todos_before_and_after_testrun_scope_session(
    test_app_before_testrun,  # noqa
    todo_requester: ToDoRequester,
):
    todos = todo_requester.validated_todo_request_admin.read_all()
    for todo in todos:
        todo_requester.validated_todo_request_admin.delete(id=todo.id)
    yield
    todos = todo_requester.validated_todo_request_admin.read_all()
    for todo in todos:
        todo_requester.validated_todo_request_admin.delete(id=todo.id)


@pytest.fixture(scope='function')
def created_todo_with_random_data() -> ToDo:
    todo = GeneratorsEntity.generate_entity_with_random_data(entity_type=ToDo)
    manager_todo.create_entity(data=todo)
    return todo


@pytest.fixture(scope='function')
def created_ten_or_more_todos_with_random_data() -> list[ToDo]:
    todos = [
        GeneratorsEntity.generate_entity_with_random_data(entity_type=ToDo)
        for _ in range(random.randint(10, 20))
    ]
    [manager_todo.create_entity(data=todo) for todo in todos]
    return todos


@pytest.fixture(scope='function')
def created_todos_with_random_data(request, todo_requester: ToDoRequester) -> list[ToDo]:
    quantity = getattr(request, 'param', 10)
    todos = [GeneratorsEntity.generate_entity_with_random_data(entity_type=ToDo) for _ in range(quantity)]
    [manager_todo.create_entity(data=todo) for todo in todos]
    return todos


@pytest.fixture(scope='function')
def todo_with_random_data_scope_test() -> ToDo:
    todo = GeneratorsEntity.generate_entity_with_random_data(entity_type=ToDo)
    manager_todo.add_data(data=todo)
    return todo


@pytest.fixture(scope='function')
def actual_todos_max_id(todo_requester: ToDoRequester) -> int:
    actual_todos = todo_requester.validated_todo_request_admin.read_all()
    return max(actual_todos, key=lambda todo: todo.id).id
