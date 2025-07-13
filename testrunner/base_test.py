from api.requests.request import HTTPSession
from config.config_general import config_general


class BaseTest:
    def __init__(self):
        self.__http_session = HTTPSession(base_url=config_general.base_url)

    @property
    def http_session(self):
        return self.__http_session