import requests

from api.rest.http_session_with_reporting import HTTPSessionWithReporting
from config.config_general import config_general
from models.creds import CredsUsernamePassword


class RESTRequest:
    def __init__(
        self, base_url: str, auth_creds: CredsUsernamePassword | None = None, timeout_ms: int = 10000
    ):
        self._base_url = base_url
        self._auth_creds = auth_creds
        self._timeput_ms = timeout_ms

        self._http_session = HTTPSessionWithReporting(
            api_session=requests.Session(),
            reporter=config_general.reporter,
        )
        if auth_creds is not None:
            self._http_session.auth = (
                self._auth_creds.username,
                self._auth_creds.password,
            )

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def session(self) -> requests.Session:
        return self._http_session
