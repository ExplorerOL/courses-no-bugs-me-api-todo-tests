import requests


class APIResponseValidator:
    def __init__(
        self,
        expected_staus_code: int = None,
        expected_body: str | None = None,
        expected_headers: dict[str, str] | None = None,
    ):
        self.__expected_status_code: int | None = expected_staus_code
        self.__expected_body: str | None = expected_body
        self.__expected_headers: dict[str, str] | None = expected_headers

    def __validate_status_code(self, actual_status_code: int) -> None:
        if self.__expected_status_code:
            assert actual_status_code == self.__expected_status_code, (
                f'Фактический статус код: {actual_status_code} не равен ожидаемому: {self.__expected_status_code}!'
            )

    def __validate_body(self, actual_body: str) -> None:
        if self.__expected_body is not None:
            assert actual_body == self.__expected_body, (
                f'Фактическое тело ответа {actual_body!r} не равно ожидаемому {self.__expected_body}!'
            )

    def __validate_headers(self, actual_headers: dict[str, str]) -> None:
        if self.__expected_headers is not None:
            for header_name, expected_header_value in self.__expected_headers.items():
                actual_header_value = actual_headers.get(header_name)
                assert actual_header_value == expected_header_value, (
                    f'Фактическое значение заголовка {header_name}: {actual_header_value!r} не равно ожидаемому: {expected_header_value}!'
                )

    def validate_response(self, response: requests.Response) -> None:
        self.__validate_status_code(actual_status_code=response.status_code)
        self.__validate_body(actual_body=response.text)
        self.__validate_headers(actual_headers=response.headers)
