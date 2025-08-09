from api.ws.ws_session_with_reporting import WSSessionWithReporting
from config.config_general import config_general
from config.endpoints import Endpoints


class WSNotification:
    def __init__(self, base_url: str, timeout_ms: int = 10000):
        self._base_url = base_url
        self._timeput_ms = timeout_ms

        self._ws_session = WSSessionWithReporting(
            uri=config_general.base_url + str(Endpoints.TODOS_NOTIFICATIONS.value),
            reporter=config_general.reporter,
        )

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def session(self) -> WSSessionWithReporting:
        return self._ws_session
