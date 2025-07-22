import requests

from models.creds import CredsUsernamePassword


class APISession:
    def __init__(
        self, base_url: str, auth_creds: CredsUsernamePassword | None = None, timeout_ms: int = 10000
    ):
        self._base_url = base_url
        self._auth_creds = auth_creds
        self._timeput_ms = timeout_ms

        self._http_session = requests.Session()
        if auth_creds is not None:
            self._http_session.auth = (self._auth_creds.username, self._auth_creds.password)

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def session(self) -> requests.Session:
        return self._http_session
