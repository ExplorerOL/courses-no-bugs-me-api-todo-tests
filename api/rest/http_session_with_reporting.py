import requests

from support.reporters.allure.reporter_protocol import ReporterProtocol


class HTTPSessionWithReporting(requests.Session):
    def __init__(self, api_session: requests.Session, reporter: ReporterProtocol):
        self._reporter = reporter
        self._session = api_session
        super().__init__()

    def send(self, request, **kwargs):
        """Отправка HTTP-запроса"""
        with self._reporter.step(f'Отправка HTTP-запроса {request.method} на URL {request.url}'):
            self._reporter.attach_text(
                f'Запрос:\n Метод: {request.method},\n URL: {request.url},\nЗаголовки:  {request.headers}\nТело: {request.body}'
            )
            response = self._session.send(request, **kwargs)
            self._reporter.attach_text(f'Ответ:\n Код: {response.status_code},\n Тело: {response.text!r}')
            return response
