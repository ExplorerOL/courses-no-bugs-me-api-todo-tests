from api.api_request import APISession
from api.todo_request import ToDoRequest
from api.validated_todo_request import ValidatedToDoRequest
from models.creds import CredsUsernamePassword


class ToDoRequestFactory:
    @staticmethod
    def __create_api_session(
        base_url: str,
        auth_creds: CredsUsernamePassword | None = None,
        timeout_ms: int = 10000,
    ) -> APISession:
        return APISession(
            base_url=base_url,
            auth_creds=auth_creds,
            timeout_ms=timeout_ms,
        )

    @staticmethod
    def create_todo_request(
        base_url: str,
        auth_creds: CredsUsernamePassword | None = None,
        is_validated: bool = False,
        timeout_ms: int = 10000,
    ) -> ToDoRequest | ValidatedToDoRequest:
        api_session = ToDoRequestFactory.__create_api_session(
            auth_creds=auth_creds,
            base_url=base_url,
            timeout_ms=timeout_ms,
        )
        if is_validated:
            return ValidatedToDoRequest(api_session=api_session)
        else:
            return ToDoRequest(api_session=api_session)
