from enum import Enum, StrEnum

from api.endpoint import Endpoint
from config.config_general import config_general


class EndpointsVersions(StrEnum):
    MOBILE = '/mobile'
    WEB = ''


class Endpoints(Enum):
    TODOS = Endpoint(
        enpoint='/todos',
        version_or_get_version_func=config_general.get_version,
    )
    TODO_BY_ID = Endpoint(
        enpoint='/todos/{todo_id}',
        version_or_get_version_func=config_general.get_version,
    )
    TODOS_NOTIFICATIONS = Endpoint(
        enpoint='/ws',
        version_or_get_version_func=config_general.get_version,
    )
