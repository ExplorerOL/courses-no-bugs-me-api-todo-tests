from functools import wraps

from api.todo_request_factory import ToDoRequestFactory
from config.config_general import config_general
from data.user_creds import user_creds
from models.todo import ToDo
from support.generator_entities import GeneratorEntities


def prepare_todos(quantity: int):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper_inner(*args, **kwargs):
            todos = [GeneratorEntities.generate_entity_with_random_data(type=ToDo) for _ in range(quantity)]
            validated_todo_request_admin = ToDoRequestFactory.create_todo_request(
                base_url=config_general.base_url,
                auth_creds=user_creds,
                is_validated=True,
            )
            [validated_todo_request_admin.create(data=todo) for todo in todos]
            return func(*args, **kwargs)

        return wrapper_inner

    return wrapper_outer
