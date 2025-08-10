import json
from contextlib import nullcontext

import pytest

from api.interfaces.notification_interface import NotificationInterface
from api.todo_notification import ToDoNotification, WSNotification
from models.todo import ToDo
from support.assertions.assert_soft import assert_soft
from support.assertions.custom_assertions import CustomAssertions


class ValidatedToDoNotification(NotificationInterface):
    def __init__(self, ws_notification: WSNotification):
        self._todo_notification = ToDoNotification(ws_notification=ws_notification)

    def read_all(self) -> list[ToDo] | None:
        """Чтение всех уведомлений"""
        notifications = self._todo_notification.read_all()
        try:
            return [ToDo(**json.loads((notification))['data']) for notification in notifications]
        except json.JSONDecodeError:
            return None

    def read_one(self) -> ToDo:
        """Чтение одного уведомления"""
        return ToDo(**json.loads(self._todo_notification.read_one())['data'])

    def verify_notification_data(self, expected_data: ToDo, soft: bool = True) -> None:
        """Проверка данных уведомления"""
        actual_todos_notification = self.read_one()
        CustomAssertions.verify_is_equal(
            actual_value=actual_todos_notification,
            expected_value=expected_data,
            soft=soft,
        )

    def verify_no_notifications_present(self, soft: bool = True) -> None:
        with assert_soft if soft else nullcontext():
            with pytest.raises(TimeoutError):
                self.read_one()
