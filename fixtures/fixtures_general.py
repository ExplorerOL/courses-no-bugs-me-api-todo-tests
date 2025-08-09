import pytest

from api.todo_requester import ToDoRequester


@pytest.fixture(scope='session')
def test_app_before_testrun(todo_requester: ToDoRequester):
    try:
        todo_requester.validated_todo_request_admin.read_all()
    except Exception as error:
        pytest.exit(reason=f'Тестовое приложение не доступно. Возникла ошибка {error}')
