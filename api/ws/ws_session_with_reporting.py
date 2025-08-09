import ssl
from typing import Protocol

from websockets.protocol import State  # noqa E402
from websockets.sync import client as ws_client

from support.reporters.allure.reporter_protocol import ReporterProtocol  # noqa E402


class WSConnectionProtocol(Protocol):
    def close(self) -> None: ...
    def recv(self, timeout: float | None = None, decode: bool | None = None) -> str | bytes: ...

    @property
    def state(self) -> int: ...


class WSSessionWithReporting:
    """Базовый класс отправителя Websocket-сообщений с использованием библиотеки Websockets"""

    WS_SESSION_OPEN_TIMEOUT = 5

    def __init__(self, uri: str, reporter: ReporterProtocol):
        self._uri: str = uri.replace('https://', 'wss://').replace('http://', 'ws://')
        self._ssl_context = None
        if self._uri.startswith('wss://'):
            self._ssl_context = ssl.SSLContext()
            self._ssl_context.verify_mode = ssl.CERT_NONE
        self._connection = self._open_connection()
        self._reporter = reporter

    def __del__(self):
        """Закрытие HTTP-сессии"""
        self.close_connection()

    def _get_connection(self) -> WSConnectionProtocol:
        if self._connection is None or self._connection.state != State.OPEN:
            self._connection = self._open_connection()
        return self._connection

    def _open_connection(self) -> WSConnectionProtocol:
        return ws_client.connect(
            uri=self._uri,
            ssl=self._ssl_context,
            open_timeout=self.WS_SESSION_OPEN_TIMEOUT,
        )

    def receive_msg(
        self,
        timeout_ms: int = 3000,
    ) -> str:
        self._connection = self._get_connection()
        msg = str(self._connection.recv(timeout=timeout_ms / 1000))
        self._reporter.attach_text(f'Уведомление: {msg!r}')
        return msg

    def close_connection(self) -> None:
        if self._connection and self._connection.state != State.CLOSED:
            self._connection.close()
