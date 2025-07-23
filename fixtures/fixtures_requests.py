import pytest

from api.todo_request_factory import ToDoRequestFactory
from api.todo_requester import ToDoRequester
from api.validated_todo_request import ValidatedToDoRequest
from config.config_general import config_general
from data.user_creds import user_creds
from models.creds import CredsUsernamePassword


@pytest.fixture(scope='session')
def validated_todo_request_wrong_auth() -> ValidatedToDoRequest:
    return ToDoRequestFactory.create_todo_request(
        base_url=config_general.base_url,
        auth_creds=CredsUsernamePassword(
            username='invalidUser',
            password='invalidPass',
        ),
        is_validated=True,
    )


@pytest.fixture(scope='session')
def todo_requester() -> ToDoRequester:
    return ToDoRequester(
        base_url=config_general.base_url,
        auth_creds=user_creds,
    )
