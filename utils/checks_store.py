from requests import Response

from resources.status_codes import StatusCode
from utils.base_checks import BaseCheckerPetstoreAPI
from utils.utils_requests import decode_response_to_json


class StoreCheckerPetstoreAPI(BaseCheckerPetstoreAPI):

    @staticmethod
    def check_order_exists(response: Response, order_id: int):
        """Existing order has its own id"""
        response_json = decode_response_to_json(response)
        StoreCheckerPetstoreAPI.check_id_in_response(response_json=response_json, _id=order_id)
        StoreCheckerPetstoreAPI.check_status_code_in_response(response=response, status_code=StatusCode.SUCCESS_OK)

    @staticmethod
    def check_order_body(response: Response, request_body: dict):
        """
        Order must has correct fields:
            - id
            - petId
            - quantity
            - complete
        """

        response_json = decode_response_to_json(response)
        try:
            for key in ('id', 'petId', 'quantity', 'complete'):
                assert response_json.get(key) == request_body.get(key)
                assert any((response_json.get(key), request_body.get(key)))
        except AssertionError:
            raise AssertionError('Response body (id, petId, quantity, complete) is different for order'
                                 f'\nresponse body: \n{response_json}'
                                 f'\n\nrequest body: \n{request_body}')

    @staticmethod
    def check_order_doesnt_exist(response):
        """For a non-existent order the error message, type and code are checked"""

        StoreCheckerPetstoreAPI.check_status_code_in_response(response=response, status_code=StatusCode.NOT_FOUND)
        response_json = decode_response_to_json(response)
        StoreCheckerPetstoreAPI.should_be_error_code_and_error_type(response_json)
        StoreCheckerPetstoreAPI.check_not_found_text_in_message_key(response_json)
