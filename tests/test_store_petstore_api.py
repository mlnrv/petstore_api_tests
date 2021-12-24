import pytest

from resources.exception_descriptions import ExceptionDescriptions
from resources.status_codes import StatusCode
from utils.checks_store import StoreCheckerPetstoreAPI
from utils.utils_petstore_api import StorePetstoreAPI
from utils.utils_requests import decode_response_to_json


class TestData:

    ID_ORDERS_INVALID = -1, 0
    ID_ORDERS_VALID = 9, 101, 999

    ORDER_DATA = {
        # 'id':
        'petId': 5,
        'quantity': 2,
        'shipDate': '2021-12-23T03:51:24.348+0000',
        'status': 'placed',
        'complete': True
    }

    URLS_STORE_ORDER_WITHOUT_ID = StorePetstoreAPI.BASE_STORE_ORDER_URL, StorePetstoreAPI.BASE_STORE_ORDER_URL + '/'


@pytest.mark.functional
class TestStorePetstoreAPI(StoreCheckerPetstoreAPI, StorePetstoreAPI):
    """
    /store/order/{orderId}
    /store/order
    """

    @pytest.fixture()
    @pytest.mark.parametrize('order_id', TestData.ID_ORDERS_VALID)
    def delete_order(self, order_id: int):
        """Delete order for placing new order"""
        self.delete_store_order(order_id=order_id)
        yield
        self.delete_store_order(order_id=order_id)

    @pytest.fixture()
    @pytest.mark.parametrize('order_id', TestData.ID_ORDERS_VALID)
    def create_order(self, order_id):
        """Create new order to work with it"""

        TestData.ORDER_DATA['id'] = order_id
        self.place_new_order(data=TestData.ORDER_DATA)
        yield {'order_data': TestData.ORDER_DATA}
        self.delete_store_order(order_id=order_id)

    @pytest.fixture()
    @pytest.mark.parametrize('order_id', TestData.ID_ORDERS_INVALID)
    def create_incorrect_orders(self, order_id):
        """Try to place incorrect order"""

        TestData.ORDER_DATA['id'] = order_id
        self.place_new_order(data=TestData.ORDER_DATA)
        yield
        self.delete_store_order(order_id=order_id)

    @pytest.mark.parametrize('url', TestData.URLS_STORE_ORDER_WITHOUT_ID)
    @pytest.mark.parametrize('request_method', ('get', 'delete'))
    def test_get_store_order_without_order_id(self, url: str, request_method: str):
        """
        /GET, /POST methods for /store/order/{orderId},
        where {order_id} is missing
        """
        self.check_expected_status_code_for_request(
            url=url, request_method=request_method, expected_status_code=StatusCode.METHOD_NOT_ALLOWED
        )

    @pytest.mark.parametrize('incorrect_order_id_type', ['id', '1.0'])
    def test_get_store_order_with_incorrect_id_type(self, incorrect_order_id_type: str):
        """
        /GET /store/order/{orderId},
        where {order_id} is not an integer
        """
        url = self.BASE_STORE_ORDER_URL + incorrect_order_id_type

        self.check_expected_status_code_for_request(
            url=url, expected_status_code=StatusCode.NOT_FOUND
        )

    @pytest.mark.parametrize('order_id', TestData.ID_ORDERS_VALID)
    def test_get_store_order(self, create_order, order_id: int):
        """Existing order has id and correct status code from the response"""
        response = self.get_store_order(order_id=order_id)

        self.check_order_exists(response=response, order_id=order_id)
        self.check_order_body(response=response, request_body=create_order['order_data'])

    @pytest.mark.parametrize('order_id', TestData.ID_ORDERS_VALID)
    def test_get_store_order_many_times_should_return_the_same_response(self, create_order, order_id: int):
        """Some orders returns different responses from time to time"""

        count_times = 10
        status_codes = [self.get_store_order(order_id=order_id).status_code for _ in range(count_times)]
        unique_status_codes = len(set(status_codes))

        assert unique_status_codes == 1, \
            f'All status code responses must be the same for one request: \nstatus codes: {status_codes}'

    @pytest.mark.parametrize('order_id', TestData.ID_ORDERS_INVALID)
    def test_get_store_order_non_existed(self, create_incorrect_orders, order_id: int):
        """Check status code, error and message for non-existed order"""
        response = self.get_store_order(order_id=order_id)

        self.check_order_doesnt_exist(response)

    @pytest.mark.parametrize('order_id', TestData.ID_ORDERS_VALID)
    def test_post_store_order(self, delete_order, order_id: int):
        """Place new order and check the data from order is correct"""

        TestData.ORDER_DATA['id'] = order_id
        response = self.place_new_order(data=TestData.ORDER_DATA)
        response_json = decode_response_to_json(response)

        self.check_status_codes(actual=response.status_code, expected=StatusCode.SUCCESS_OK)

        assert TestData.ORDER_DATA == response_json, \
            f'{ExceptionDescriptions.DIFF_RESPONSE_AND_BODY}' \
            f'{TestData.ORDER_DATA}\n!= \n{response_json}'
