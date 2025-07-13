import requests

from api.rest.models.models import CredsUsernamePassword


class HTTPSession(requests.Session):
    def __new__(cls):
        if HTTPSession.__instance is None:
            HTTPSession.__instance = super().__new__(cls)
            return HTTPSession.__instance
        else:
            return HTTPSession.__instance

    def __init__(
        self,
        base_url: str,
        verify_ssl: bool = False,
    ):
        self.__base_url = base_url
        self.__session = requests.Session()
        self.__session.verify = verify_ssl

    # @property
    # def session(self):
    #     return self.__session

    @property
    def base_url(self):
        return self.__base_url


class Request:
    def __init__(
        self,
        http_session: HTTPSession,
        auth_creds: CredsUsernamePassword | None = None,
    ):
        self.__http_session: HTTPSession = http_session
        self.__auth_creds = auth_creds
