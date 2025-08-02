from json import JSONDecodeError

from api.api_request import APIRequest
from api.interfaces.crud_interface import CRUDInterface
from api.response_validators.api_response_validator import APIResponseValidator
from api.response_validators.api_response_validators_templates import APIResponseValidatorsTemplates
from api.todo_request import ToDoRequest
from models.todo import ToDo
from support.assertions.custom_assertions import CustomAssertions
from support.reporters.allure.reporter_base_classes import ClassWithMethodReporting
from support.reporters.allure.reporter_metaclasses import MetaclassABCMetaWithMethodReporting


class ValidatedToDoRequest(
    CRUDInterface,
    ClassWithMethodReporting,
    metaclass=MetaclassABCMetaWithMethodReporting,
):
    def __init__(self, api_session: APIRequest):
        self.__todo_request = ToDoRequest(api_request=api_session)

    def create(
        self,
        data: ToDo,
        response_validator: APIResponseValidator = APIResponseValidatorsTemplates.status_created_body_empty,
        soft_validation: bool = False,
    ) -> str:
        """Отправка запроса на создание с валидацией ответа"""
        response = self.__todo_request.create(data=data)
        response_validator.validate_response(response=response, soft=soft_validation)
        return response.text

    def update(
        self,
        id: int,
        data: ToDo,
        response_validator: APIResponseValidator = APIResponseValidatorsTemplates.status_ok_body_empty,
        soft_validation: bool = False,
    ) -> None:
        """Отправка запроса на обновление с валидацией ответа"""
        response = self.__todo_request.update(id=id, data=data)
        response_validator.validate_response(response=response, soft=soft_validation)

    def delete(
        self,
        id: int,
        response_validator: APIResponseValidator = APIResponseValidatorsTemplates.status_no_content_body_empty,
        soft_validation: bool = False,
    ) -> str:
        """Отправка запроса на удаление с валидацией ответа"""
        response = self.__todo_request.delete(id=id)
        response_validator.validate_response(response=response, soft=soft_validation)
        return response.text

    def read_all(
        self,
        offset: int | None = None,
        limit: int | None = None,
        response_validator: APIResponseValidator = APIResponseValidatorsTemplates.status_ok_header_json,
        soft_validation: bool = False,
    ) -> list[ToDo] | None:
        """Отправка запроса на чтение всех сущностей с валидацией ответа"""
        if all([offset is not None, limit is not None]):
            response = self.__todo_request.read_all(limit=limit, offset=offset)
        else:
            response = self.__todo_request.read_all()

        response_validator.validate_response(response=response, soft=soft_validation)
        try:
            body_json = response.json()
            return [ToDo(**todo) for todo in body_json]
        except JSONDecodeError:
            return None

    def verify_todos_count(self, expected_count: int, soft: bool = True) -> None:
        """Проверка количество TODO равно ожидаемому"""
        actual_todos_count = len(self.read_all())
        CustomAssertions.verify_is_equal(
            actual_value=actual_todos_count,
            expected_value=expected_count,
            soft=soft,
        )

    def verify_todo_data(self, todo_id: int, expected_data: ToDo, soft: bool = True) -> None:
        """Проверка данных TODO"""
        EXPECTED_FOUND_TODOS_COUNT = 1
        actual_todos = self.read_all()
        found_todo = list(filter(lambda todo: todo.id == todo_id, actual_todos))
        CustomAssertions.verify_is_equal(
            actual_value=len(found_todo),
            expected_value=EXPECTED_FOUND_TODOS_COUNT,
            soft=soft,
        )
        CustomAssertions.verify_is_equal(
            actual_value=found_todo[0],
            expected_value=expected_data,
            soft=soft,
        )
