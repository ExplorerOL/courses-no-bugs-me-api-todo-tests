from enum import StrEnum


class Endpoints(StrEnum):
    todos = '/todos'
    todo_by_id = '/todos/{todo_id}'
