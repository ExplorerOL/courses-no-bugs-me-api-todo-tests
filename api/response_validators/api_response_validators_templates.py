from http import HTTPStatus

from api.response_validators.api_response_validator import APIResponseValidator


class APIResponseValidatorsTemplates:
    status_ok_body_empty = APIResponseValidator(
        expected_staus_code=HTTPStatus.OK,
        expected_body='',
    )
    status_ok_header_json = APIResponseValidator(
        expected_staus_code=HTTPStatus.OK,
        expected_headers={'Content-Type': 'application/json'},
    )
    status_created_body_empty = APIResponseValidator(
        expected_staus_code=HTTPStatus.CREATED,
        expected_body='',
    )
    status_no_content_body_empty = APIResponseValidator(
        expected_staus_code=HTTPStatus.NO_CONTENT,
        expected_body='',
    )
    status_unauthorized = APIResponseValidator(expected_staus_code=HTTPStatus.UNAUTHORIZED)
    status_not_found = APIResponseValidator(expected_staus_code=HTTPStatus.NOT_FOUND)
    status_not_found_body_empty = APIResponseValidator(
        expected_staus_code=HTTPStatus.NOT_FOUND,
        expected_body='',
    )
    status_bad_req = APIResponseValidator(expected_staus_code=HTTPStatus.BAD_REQUEST)
    status_bad_req_body_empty = APIResponseValidator(
        expected_staus_code=HTTPStatus.BAD_REQUEST,
        expected_body='',
    )
    status_bad_req_body_invalid_query_string = APIResponseValidator(
        expected_staus_code=HTTPStatus.BAD_REQUEST,
        expected_headers={'Content-Type': 'text/plain; charset=utf-8'},
        expected_body='Invalid query string',
    )
