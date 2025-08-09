from api.factory_requests import FactoryRequests
from api.todo_request import ToDoRequest
from api.validated_todo_notification import ValidatedToDoNotification
from api.validated_todo_request import ValidatedToDoRequest
from config.config_general import config_general
from data.user_creds import user_creds
from models.creds import CredsUsernamePassword


class ToDoRequester:
    def __init__(
        self,
        base_url: str,
        auth_creds: CredsUsernamePassword | None = None,
        timeout_ms: int = 10000,
    ):
        self.__todo_request_anonim = FactoryRequests.create_todo_request(
            base_url=base_url,
            timeout_ms=timeout_ms,
        )
        self.__todo_request_admin = FactoryRequests.create_todo_request(
            base_url=base_url,
            auth_creds=auth_creds,
            timeout_ms=timeout_ms,
        )
        self.__validated_todo_request_anonim = FactoryRequests.create_todo_request(
            base_url=base_url,
            timeout_ms=timeout_ms,
            is_validated=True,
        )
        self.__validated_todo_request_admin = FactoryRequests.create_todo_request(
            base_url=base_url,
            auth_creds=auth_creds,
            timeout_ms=timeout_ms,
            is_validated=True,
        )
        self.__validated_todo_notification_anonim = FactoryRequests.create_todo_notification(
            base_url=base_url,
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

    @property
    def validated_todo_notification_anonim(self) -> ValidatedToDoNotification:
        return self.__validated_todo_notification_anonim


todo_requester = ToDoRequester(
    base_url=config_general.base_url,
    auth_creds=user_creds,
)
