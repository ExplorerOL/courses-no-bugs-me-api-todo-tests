import pytest

from api.todo_request import ToDoRequest
from api.validated_todo_request import ValidatedToDoRequest
from config.config_general import config_general
from data.user_creds import user_creds
from models.creds import CredsUsernamePassword


@pytest.fixture(scope='session')
def todo_request_admin() -> ToDoRequest:
    return ToDoRequest(
        base_url=config_general.base_url,
        auth_creds=user_creds,
    )


@pytest.fixture(scope='session')
def validated_todo_request_wrong_auth() -> ValidatedToDoRequest:
    return ValidatedToDoRequest(
        base_url=config_general.base_url,
        auth_creds=CredsUsernamePassword(
            username='invalidUser',
            password='invalidPass',
        ),
    )


@pytest.fixture(scope='session')
def validated_todo_request_anonim() -> ValidatedToDoRequest:
    return ValidatedToDoRequest(base_url=config_general.base_url)


@pytest.fixture(scope='session')
def validated_todo_request_admin() -> ValidatedToDoRequest:
    return ValidatedToDoRequest(
        base_url=config_general.base_url,
        auth_creds=user_creds,
    )
