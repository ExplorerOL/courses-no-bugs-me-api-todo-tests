from functools import wraps

from api.validated_todo_request import ValidatedToDoRequest
from config.config_general import config_general
from data.user_creds import user_creds
from support.generators_todo import GeneratorsToDo


def prepare_todos(quantity: int):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper_inner(*args, **kwargs):
            todos = [GeneratorsToDo.generate_todo_with_random_data() for _ in range(quantity)]
            validated_todo_request_admin = ValidatedToDoRequest(
                base_url=config_general.base_url,
                auth_creds=user_creds,
            )
            [validated_todo_request_admin.create(data=todo) for todo in todos]
            return func(*args, **kwargs)

        return wrapper_inner

    return wrapper_outer
