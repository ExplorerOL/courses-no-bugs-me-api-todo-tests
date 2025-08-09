from api.rest.rest_request import RESTRequest
from api.todo_notification import WSNotification
from api.todo_request import ToDoRequest
from api.validated_todo_notification import ValidatedToDoNotification
from api.validated_todo_request import ValidatedToDoRequest
from models.creds import CredsUsernamePassword


class FactoryRequests:
    @staticmethod
    def __create_rest_request(
        base_url: str,
        auth_creds: CredsUsernamePassword | None = None,
        timeout_ms: int = 10000,
    ) -> RESTRequest:
        return RESTRequest(
            base_url=base_url,
            auth_creds=auth_creds,
            timeout_ms=timeout_ms,
        )

    @staticmethod
    def __create_ws_notification(
        base_url: str,
        timeout_ms: int = 10000,
    ) -> WSNotification:
        return WSNotification(
            base_url=base_url,
            timeout_ms=timeout_ms,
        )

    @staticmethod
    def create_todo_request(
        base_url: str,
        auth_creds: CredsUsernamePassword | None = None,
        is_validated: bool = False,
        timeout_ms: int = 10000,
    ) -> ToDoRequest | ValidatedToDoRequest:
        rest_request = FactoryRequests.__create_rest_request(
            auth_creds=auth_creds,
            base_url=base_url,
            timeout_ms=timeout_ms,
        )
        if is_validated:
            return ValidatedToDoRequest(rest_request=rest_request)
        else:
            return ToDoRequest(rest_request=rest_request)

    @staticmethod
    def create_todo_notification(
        base_url: str,
        is_validated: bool = False,
        timeout_ms: int = 10000,
    ) -> WSNotification | ValidatedToDoNotification:
        ws_notification = FactoryRequests.__create_ws_notification(
            base_url=base_url,
            timeout_ms=timeout_ms,
        )
        if is_validated:
            return ValidatedToDoNotification(ws_notification=ws_notification)
        else:
            return WSNotification(ws_notification=ws_notification)
