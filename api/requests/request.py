import requests

from api.rest.models.models import CredsUsernamePassword


class HTTPSession(requests.Session):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Request:
    def __init__(
        self,
        base_url: str,
        auth_creds: CredsUsernamePassword | None = None,
    ):
        print('Init TodoRequest')
        self._base_url = base_url
        self._auth_creds = auth_creds

        print('Init http session')
        self._http_session = HTTPSession()
        print(f'HTTPSession = {self._http_session!r}')
        if auth_creds is not None:
            self._http_session.auth = (self._auth_creds.username, self._auth_creds.password)
