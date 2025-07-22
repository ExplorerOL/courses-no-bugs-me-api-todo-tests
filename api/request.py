import requests

from models.creds import CredsUsernamePassword


class Request:
    def __init__(
        self, base_url: str, auth_creds: CredsUsernamePassword | None = None, timeout_ms: int = 10000
    ):
        self._base_url = base_url
        self._auth_creds = auth_creds
        self._timeput_ms = timeout_ms

        self._http_session = requests.Session()
        if auth_creds is not None:
            self._http_session.auth = (self._auth_creds.username, self._auth_creds.password)
