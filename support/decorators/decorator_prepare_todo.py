from functools import wraps

from managers.manager_todo import manager_todo
from models.todo import ToDo
from support.generators_entity import GeneratorEntities


def prepare_todos(quantity: int):
    def wrapper_outer(func):
        @wraps(func)
        def wrapper_inner(*args, **kwargs):
            todos = [GeneratorEntities.generate_entity_with_random_data(type=ToDo) for _ in range(quantity)]
            # validated_todo_request_admin = FactoryRequests.create_todo_request(
            #     base_url=config_general.base_url,
            #     auth_creds=user_creds,
            #     is_validated=True,
            # )
            [manager_todo.create_entity(data=todo) for todo in todos]
            return func(*args, **kwargs)

        return wrapper_inner

    return wrapper_outer
