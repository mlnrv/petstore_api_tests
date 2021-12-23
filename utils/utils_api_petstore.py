from utils.utils_requests import make_request


class PetstoreAPI:

    BASE_URL = 'https://petstore.swagger.io/v2'
    BASE_STORE_ORDER_URL = BASE_URL + '/store/order'

    @staticmethod
    def get_store_order(order_id: int):
        """
        Send request /GET /store/order/{orderId} and return response
        """
        url = PetstoreAPI.BASE_STORE_ORDER_URL + f'/{order_id}'
        return make_request(url=url)

    @staticmethod
    def delete_store_order(order_id: int):
        """
        Send request /DELETE /store/order/{orderId} and return response
        """
        url = PetstoreAPI.BASE_STORE_ORDER_URL + f'/{order_id}'
        return make_request(url=url, method='post')
