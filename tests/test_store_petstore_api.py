import pytest

from utils.checks_api_petstore import StoreCheckerPetstoreAPI
from utils.utils_api_petstore import PetstoreAPI


@pytest.mark.functional
class TestStorePetstoreAPI(StoreCheckerPetstoreAPI):

    EXISTING_ORDERS = (1, 2)
    NON_EXISTED_ORDERS = (-1, 0, 100)
    URLS_STORE_ORDER_WITHOUT_ORDER_ID = (PetstoreAPI.BASE_STORE_ORDER_URL, PetstoreAPI.BASE_STORE_ORDER_URL + '/')

    @pytest.fixture()
    def prepare_orders(self):
        pass

    @pytest.mark.parametrize('url', URLS_STORE_ORDER_WITHOUT_ORDER_ID)
    @pytest.mark.parametrize('request_method', ('get', 'delete'))
    def test_get_store_order_without_order_id(self, url, request_method):
        StoreCheckerPetstoreAPI.check_error_while_store_order_without_order_id(url=url, request_method=request_method)

    @pytest.mark.skip('needs preparation for orders getting')
    @pytest.mark.parametrize('order_id', EXISTING_ORDERS)
    def test_get_existing_store_order(self, order_id):
        response = PetstoreAPI.get_store_order(order_id=order_id)
        self.check_order_exists(response=response, order_id=order_id)

    @pytest.mark.skip('needs preparation for orders getting')
    @pytest.mark.parametrize('order_id', NON_EXISTED_ORDERS)
    def test_get_non_existed_store_order(self, order_id):
        response = PetstoreAPI.get_store_order(order_id=order_id)
        self.check_order_doesnt_exist(response)
