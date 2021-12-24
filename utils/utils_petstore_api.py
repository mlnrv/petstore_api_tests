from random import randint

from resources.status_codes import StatusCode
from utils.utils_requests import send_request


class StorePetstoreAPI:

    BASE_URL = 'https://petstore.swagger.io/v2'
    BASE_STORE_ORDER_URL = BASE_URL + '/store/order'

    @staticmethod
    def get_store_order(order_id: int):
        """
        Get an order info and return response
        /store/order/{orderId}
        """
        url = StorePetstoreAPI.BASE_STORE_ORDER_URL + f'/{order_id}'
        return send_request(url=url)

    @staticmethod
    def delete_store_order(order_id: int):
        """
        Delete the order and return response
        /store/order/{orderId}
        """
        url = StorePetstoreAPI.BASE_STORE_ORDER_URL + f'/{order_id}'
        return send_request(url=url, method='delete')

    @staticmethod
    def post_store_order(data):
        """
        Place an order  and return response
        /store/order/
        """
        url = StorePetstoreAPI.BASE_STORE_ORDER_URL
        headers = {'content-type': 'application/json'}
        response = send_request(url=url, method='post', headers=headers, data=data, send_as_json=True)
        return response

    @staticmethod
    def place_new_order(data: dict):
        """Tries to find free id to place new order. If it finds, then place new order"""

        order_id = randint(100, 999) if not data.get('id') else data.get('id')
        # check that order id is free
        response_get_order = StorePetstoreAPI.get_store_order(order_id=order_id)
        if response_get_order.status_code != StatusCode.NOT_FOUND:
            raise InterruptedError(f'Order id={order_id} must not be found'
                                   f'\nresponse: {response_get_order.text}')

        # place new order
        response_post_order = StorePetstoreAPI.post_store_order(data=data)
        if response_post_order.status_code != StatusCode.SUCCESS_OK:
            raise InterruptedError('An error occurred while placing an order:'
                                   f'\nresponse: {response_post_order}'
                                   f'\n\ndata: {data}')
        return response_post_order
