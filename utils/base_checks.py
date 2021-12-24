from requests.models import Response

from resources.exception_descriptions import ExceptionDescriptions
from utils.utils_requests import send_request


ERROR_CODE = 1
ERROR_TYPE = 'error'


class BaseCheckerPetstoreAPI:

    @staticmethod
    def check_not_found_text_in_message_key(_response_json: dict):
        actual_message = _response_json.get('message')

        assert 'not found' in actual_message.lower(), \
            f'Key "message" must contain text "not found" in the response body: ' \
            f'\nresponse: {_response_json}'

    @staticmethod
    def check_status_code_in_response(response: Response, status_code: int):
        """Compare status code from response and expected status code"""

        actual_status_code, expected_status_code = response.status_code, status_code
        assert actual_status_code == expected_status_code, \
            f'{ExceptionDescriptions.DIFF_STATUS_CODES}:' \
            f'\n{actual_status_code} != {expected_status_code} ' \
            f'\nresponse: {response.text}'

    @staticmethod
    def should_be_error_code_and_error_type(response_json: dict):
        actual_code, expected_code = response_json.get('code'), ERROR_CODE
        assert actual_code == expected_code, \
            f'{ExceptionDescriptions.BODY_ERROR_CODES}:' \
            f'{actual_code}\n!= \n{expected_code}'

        actual_type, expected_type = response_json.get('type'), ERROR_TYPE
        assert actual_type == expected_type, \
            f'{ExceptionDescriptions.BODY_ERROR_TYPES}:' \
            f'{actual_type}\n!= \n{expected_type}'

    @staticmethod
    def check_id_in_response(response_json: dict, _id: int):
        assert response_json.get('id') == _id, \
            f'Order has an unexpected id: {response_json.get("id")}' \
            f'\nExpected id: {_id}'

    @staticmethod
    def check_status_codes(actual: int, expected: int):
        assert actual == expected, \
            f'{ExceptionDescriptions.DIFF_STATUS_CODES}' \
            f'{actual}\n!= \n{expected}'

    @staticmethod
    def check_expected_status_code_for_request(url: str, expected_status_code: int, request_method: str = 'get'):
        """Expects Method Not Allowed while sending request without order id"""
        response = send_request(url=url, method=request_method)

        assert response.status_code == expected_status_code, \
            f'{ExceptionDescriptions.DIFF_STATUS_CODES}:' \
            f'\n{response.status_code} != {expected_status_code}'
