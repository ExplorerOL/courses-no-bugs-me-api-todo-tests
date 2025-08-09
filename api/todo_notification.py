from api.interfaces.search_interface import SearchInterface
from api.ws.ws_notification import WSNotification
from support.reporters.allure.reporter_metaclasses import MetaclassABCMetaWithMethodReporting


class ToDoNotification(
    SearchInterface,
    metaclass=MetaclassABCMetaWithMethodReporting,
):
    def __init__(self, ws_notification: WSNotification):
        self._ws_notification = ws_notification

    def read_all(self, timeout_ms: int = 500) -> list[str]:
        notifications = []
        try:
            while True:
                msg = self._ws_notification.session.receive_msg(timeout_ms=timeout_ms)
                notifications.append(msg)
        except TimeoutError:
            pass
        return notifications

    def read_one(self, timeout_ms: int = 500) -> str:
        return self._ws_notification.session.receive_msg(timeout_ms=timeout_ms)
