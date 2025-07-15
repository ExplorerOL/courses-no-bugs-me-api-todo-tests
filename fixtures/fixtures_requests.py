import pytest

from config.config_general import config_general
from data.creds import auth_user_creds
from src.todo.requests.todo_request import ToDoRequest
from src.todo.requests.validated_todo_request import ValidatedToDoRequest


@pytest.fixture(scope='session')
def todo_request() -> ToDoRequest:
    return ToDoRequest(
        base_url=config_general.base_url,
        auth_creds=auth_user_creds,
    )


@pytest.fixture(scope='session')
def validated_todo_request() -> ToDoRequest:
    return ValidatedToDoRequest(
        base_url=config_general.base_url,
        auth_creds=auth_user_creds,
    )
