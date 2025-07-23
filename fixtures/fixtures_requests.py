import pytest

from api.factory_requests import FactoryRequests
from api.todo_requester import ToDoRequester
from api.todo_requester import todo_requester as todo_requester_obj
from api.validated_todo_request import ValidatedToDoRequest
from config.config_general import config_general
from models.creds import CredsUsernamePassword


@pytest.fixture(scope='session')
def validated_todo_request_wrong_auth() -> ValidatedToDoRequest:
    return FactoryRequests.create_todo_request(
        base_url=config_general.base_url,
        auth_creds=CredsUsernamePassword(
            username='invalidUser',
            password='invalidPass',
        ),
        is_validated=True,
    )


@pytest.fixture(scope='session')
def todo_requester() -> ToDoRequester:
    return todo_requester_obj
