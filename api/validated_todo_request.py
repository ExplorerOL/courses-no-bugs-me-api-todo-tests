from json import JSONDecodeError

from api.interfaces.crud_interface import CRUDInterface
from api.interfaces.search_interface import SearchInterface
from api.request import Request
from api.response_validators.api_response_validator import APIResponseValidator
from api.response_validators.api_response_validators import APIResponseValidators
from api.todo_request import ToDoRequest
from models.creds import CredsUsernamePassword
from models.todo import ToDo
from storages.tst_data_storage import TstDataStorage


class ValidatedToDoRequest(Request, CRUDInterface, SearchInterface):
    def __init__(self, base_url: str, auth_creds: CredsUsernamePassword | None = None):
        super().__init__(base_url=base_url, auth_creds=auth_creds)
        self.__todo_request = ToDoRequest(base_url=self._base_url, auth_creds=self._auth_creds)

    def create(
        self,
        data: ToDo,
        response_validator: APIResponseValidator = APIResponseValidators.status_created_body_empty,
    ) -> str:
        response = self.__todo_request.create(data=data)
        response_validator.validate_response(response=response)

        TstDataStorage().add_data(data=data)
        return response.text

    def update(
        self,
        id: int,
        data: ToDo,
        response_validator: APIResponseValidator = APIResponseValidators.status_ok_body_empty,
    ) -> None:
        response = self.__todo_request.update(id=id, data=data)
        response_validator.validate_response(response=response)

    def delete(
        self,
        id: int,
        response_validator: APIResponseValidator = APIResponseValidators.status_no_content_body_empty,
    ) -> str:
        response = self.__todo_request.delete(id=id)
        response_validator.validate_response(response=response)
        return response.text

    def read_all(
        self,
        offset: int | None = None,
        limit: int | None = None,
        response_validator: APIResponseValidator = APIResponseValidators.status_ok_header_json,
    ) -> list[ToDo] | None:
        if all([offset is not None, limit is not None]):
            response = self.__todo_request.read_all(limit=limit, offset=offset)
        else:
            response = self.__todo_request.read_all()

        response_validator.validate_response(response=response)
        try:
            body_json = response.json()
            return [ToDo(**todo) for todo in body_json]
        except JSONDecodeError:
            return None
