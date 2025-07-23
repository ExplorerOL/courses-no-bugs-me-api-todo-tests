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
