import pytest

from api.todo_requester import ToDoRequester
from fixtures.fixtures_todo import created_todo_with_random_data  # noqa


@pytest.fixture(scope='function')
def delete_all_notifications_before_test_scope_test(
    created_todo_with_random_data,  # noqa
    todo_requester: ToDoRequester,
) -> None:
    todo_requester.validated_todo_notification_anonim.read_all()
