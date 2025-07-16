from http import HTTPStatus

from src.models.creds import CredsUsernamePassword
from src.models.todo import ToDo
from src.todo.requests.crud_interface import CRUDInterface
from src.todo.requests.request import Request
from src.todo.requests.search_interface import SearchInterface
from src.todo.requests.todo_request import ToDoRequest


class ValidatedToDoRequest(Request, CRUDInterface, SearchInterface):
    def __init__(self, base_url: str, auth_creds: CredsUsernamePassword | None = None):
        super().__init__(base_url=base_url, auth_creds=auth_creds)
        self.__todo_request = ToDoRequest(base_url=self._base_url, auth_creds=self._auth_creds)

    def create(self, data: ToDo) -> str:
        response = self.__todo_request.create(data=data)
        assert response.status_code == HTTPStatus.CREATED
        assert response.text == ''
        return response.text

    def update(self, id: int, data: ToDo) -> None:
        response = self.__todo_request.update(id=id, data=data)
        assert response.status_code == HTTPStatus.OK

    def delete(self, id: int) -> str:
        response = self.__todo_request.delete(id=id)
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert response.text == ''
        return response.text

    def read_all(self, offset: int | None = None, limit: int | None = None) -> list[ToDo]:
        if all([offset is not None, limit is not None]):
            response = self.__todo_request.read_all(limit=limit, offset=offset)
        else:
            response = self.__todo_request.read_all()

        assert response.status_code == HTTPStatus.OK
        assert response.headers['Content-Type'] == 'application/json'
        body_json = response.json()
        return [ToDo(**todo) for todo in body_json]
