from api.todo_request import ToDoRequest
from api.todo_request_factory import ToDoRequestFactory
from api.validated_todo_request import ValidatedToDoRequest
from models.creds import CredsUsernamePassword


class ToDoRequester:
    def __init__(
        self,
        base_url: str,
        auth_creds: CredsUsernamePassword | None = None,
        timeout_ms: int = 10000,
    ):
        self.__todo_request_anonim = ToDoRequestFactory.create_todo_request(
            base_url=base_url,
            timeout_ms=timeout_ms,
        )
        self.__todo_request_admin = ToDoRequestFactory.create_todo_request(
            base_url=base_url,
            auth_creds=auth_creds,
            timeout_ms=timeout_ms,
        )
        self.__validated_todo_request_anonim = ToDoRequestFactory.create_todo_request(
            base_url=base_url,
            timeout_ms=timeout_ms,
            is_validated=True,
        )
        self.__validated_todo_request_admin = ToDoRequestFactory.create_todo_request(
            base_url=base_url,
            auth_creds=auth_creds,
            timeout_ms=timeout_ms,
            is_validated=True,
        )

    @property
    def todo_request_anonim(self) -> ToDoRequest:
        return self.__todo_request_anonim

    @property
    def todo_request_admin(self) -> ToDoRequest:
        return self.__todo_request_admin

    @property
    def validated_todo_request_anonim(self) -> ValidatedToDoRequest:
        return self.__validated_todo_request_anonim

    @property
    def validated_todo_request_admin(self) -> ValidatedToDoRequest:
        return self.__validated_todo_request_admin
