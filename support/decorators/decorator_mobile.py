from functools import wraps

from config.config_general import config_general
from config.endpoints import EndpointsVersions


def mobile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        config_general.set_version(version=EndpointsVersions.MOBILE)
        result = func(*args, **kwargs)
        config_general.set_version(version=EndpointsVersions.WEB)
        return result

    return wrapper
