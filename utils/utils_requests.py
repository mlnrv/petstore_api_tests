from json.decoder import JSONDecodeError
from requests import request


def decode_response_to_json(response):
    """Decode response body to json"""
    try:
        return response.json()
    except JSONDecodeError:
        raise InterruptedError('JSONDecodeError occurred while converting response to json:'
                               f'\nresponse: {response}')


def send_request(url: str, method: str = 'get', auth: tuple = None,
                 data: dict = None, headers: dict = None, send_as_json: bool = False):
    """Send request (using requests library) and return response"""

    params = {
        'url': url,
        'method': method,
        'auth': auth,
        'headers': headers
    }
    try:
        if send_as_json:
            response = request(**params, json=data)
        else:
            response = request(**params, data=data)
    except Exception:
        raise InterruptedError(f'Error while sending a request:'
                               f'\nwith params: \n"{params}"'
                               f'\nand data: \n"{data}"')
    return response
