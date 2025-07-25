import requests

from support.reporters.allure.reporter_protocol import ReporterProtocol


class APISessionWithReporting(requests.Session):
    def __init__(self, api_session: requests.Session, reporter: ReporterProtocol):
        self._reporter = reporter
        self._session = api_session
        super().__init__()

    def send(self, request, **kwargs):
        with self._reporter.step(
            f"""
            Отправка запроса {request.method} на URL {request.url}\n
            Заголовки:  {request.headers}\n
            Тело: {request.body}""",
        ):
            return self._session.send(request, **kwargs)
