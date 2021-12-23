from requests.models import Response

from resources.exception_descriptions import ExceptionDescriptions
from resources.status_codes import StatusCode
from utils.utils_requests import decode_response_to_json, make_request


ERROR_CODE = 1
ERROR_TYPE = 'error'


class BaseCheckerPetstoreAPI:

    @staticmethod
    def check_status_code_in_response(response: Response, status_code: int):
        """Compare status code from response and expected status code"""

        actual_status_code, expected_status_code = response.status_code, status_code
        assert actual_status_code == expected_status_code, \
            f'{ExceptionDescriptions.DIFFERENT_RESPONSE_STATUS_CODES}:' \
            f'\n{actual_status_code} != {expected_status_code} ' \
            f'\nresponse: {response.text}'

    @staticmethod
    def should_be_error_code_and_error_type(response_json: dict):
        actual_code, expected_code = response_json.get('code'), ERROR_CODE
        assert actual_code == expected_code, \
            f'{ExceptionDescriptions.DIFFERENT_BODY_ERROR_CODES}:' \
            f'{actual_code}\n!= \n{expected_code}'

        actual_type, expected_type = response_json.get('type'), ERROR_TYPE
        assert actual_type == expected_type, \
            f'{ExceptionDescriptions.DIFFERENT_BODY_ERROR_TYPES}:' \
            f'{actual_type}\n!= \n{expected_type}'

    @staticmethod
    def check_id_in_response(response_json: dict, _id: int):
        assert response_json.get('id') == _id


class StoreCheckerPetstoreAPI(BaseCheckerPetstoreAPI):
    MESSAGE_ORDER_NOT_FOUND = 'Order not found'

    @staticmethod
    def check_order_exists(response: Response, order_id: int):
        """Existing order has its own id"""

        BaseCheckerPetstoreAPI.check_status_code_in_response(response=response, status_code=StatusCode.SUCCESS_OK)
        response_json = decode_response_to_json(response)
        assert response_json.get('id') == order_id, \
            f'Order has an unexpected id: {response_json.get("id")}' \
            f'\nExpected id: {order_id}'

    @staticmethod
    def check_order_doesnt_exist(response):
        """For a non-existent order the error message, type and code are checked"""

        def check_message_order_not_found(_response_json: dict):
            actual_message = _response_json.get('message')
            expected_message = StoreCheckerPetstoreAPI.MESSAGE_ORDER_NOT_FOUND
            assert actual_message == expected_message, \
                f'Unexpected message for non-existed order: ' \
                f'\n"{actual_message}"\n != \n"{expected_message}"'

        BaseCheckerPetstoreAPI.check_status_code_in_response(response=response,
                                                             status_code=StatusCode.CLIENT_ERROR_NOT_FOUND)

        response_json = decode_response_to_json(response)
        BaseCheckerPetstoreAPI.should_be_error_code_and_error_type(response_json)
        check_message_order_not_found(response_json)

    @staticmethod
    def check_error_while_store_order_without_order_id(url: str, request_method: str):
        """Expects Method Not Allowed while sending request without order id"""

        response = make_request(url=url, method=request_method)
        actual_status_code, expected_status_code = response.status_code, StatusCode.CLIENT_METHOD_NOT_ALLOWED

        assert actual_status_code == expected_status_code, \
            f'{ExceptionDescriptions.DIFFERENT_RESPONSE_STATUS_CODES}:' \
            f'\n{actual_status_code} != {expected_status_code}'
