import os

import pytest

from api.todo_requester import ToDoRequester
from config.config_general import config_general


@pytest.fixture(scope='session')
def test_app_before_testrun(todo_requester: ToDoRequester):
    try:
        todo_requester.validated_todo_request_admin.read_all()
    except Exception as error:
        pytest.exit(reason=f'Тестовое приложение не доступно. Возникла ошибка {error}')


@pytest.fixture(scope='function', autouse=True)
def before_each_test():
    full_test_name = os.environ.get('PYTEST_CURRENT_TEST')
    test_dir_path_str = full_test_name.split('::')[0]
    test_dir_path_str_splited = test_dir_path_str.split('/')
    if len(test_dir_path_str_splited) > 1:
        suite_name = test_dir_path_str_splited[-2]
        config_general.reporter.set_suite(suite_name=suite_name)
    if len(test_dir_path_str_splited) > 2:
        parent_suite_name = test_dir_path_str_splited[-3]
        config_general.reporter.set_parent_suite(parent_suite_name=parent_suite_name)
