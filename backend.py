import abc
import json

import requests

import utils

LOG = utils.get_logger(__file__)
BASE = 'http://cec2019.ca'
API_TOKEN = 'brunswick-8Nq9JsYFUtFzdReih3P8s2YMQiRQHDRMkWNkASN5A8xMGa4yzq5njUv4hFEEaBbZ'
PATH = '/tmp/instance.json'
ENABLE_FRONTEND = False


# noinspection PyShadowingBuiltins
class IBackend(abc.ABC):
    @abc.abstractmethod
    def create_instance(self):
        pass

    @abc.abstractmethod
    def get_instance(self):
        pass

    @abc.abstractmethod
    def delete_instance(self):
        pass

    @abc.abstractmethod
    def finish(self):
        pass

    @abc.abstractmethod
    def turn(self, direction):
        pass

    @abc.abstractmethod
    def move(self):
        pass

    @abc.abstractmethod
    def scan(self):
        pass

    @abc.abstractmethod
    def collect_item(self, id):
        pass

    @abc.abstractmethod
    def unload_item(self, id):
        pass


class RuntimeFailure(RuntimeError):
    pass


def request(method, url):
    """
    Request Wrappers for Attaching API Token

    :param method: The method.
    :param url: The url.
    :return: The response.
    """
    # print(f'{method} -> {url}')
    res = requests.request(method, BASE + url, headers={'token': API_TOKEN})
    body = res.json()

    t = body['type']
    # print(f'\r{method} -> {t}')
    if t == 'ERROR':
        raise RuntimeError(body['message'])

    if t == 'FAILURE':
        raise RuntimeFailure(body['message'])

    if t != 'SUCCESS':
        raise RuntimeError(f'Unknown type: {t}')

    if body['payload'] is not None:
        if ENABLE_FRONTEND:
            requests.request('POST', 'http://localhost:3000/update', headers={'content-type': 'application/json'},  data=json.dumps(body['payload']))

    return body['payload']


def get(url):
    return request('GET', url)


def delete(url):
    return request('DELETE', url)


def post(url):
    return request('POST', url)


# noinspection PyMethodMayBeStatic,PyShadowingBuiltins
class Backend(IBackend):
    """
    Create the current instance
    """
    def create_instance(self):
        return post('/instance')

    """
    Retrieve the current instance
    """
    def get_instance(self):
        return get('/instance')

    """
    Delete the current instance, and notify the frontend
    """
    def delete_instance(self):
        if ENABLE_FRONTEND:
            requests.request('POST', 'http://localhost:3000/close')
        return delete('/instance')

    """
    Declare collection complete
    """
    def finish(self):
        return post('/finish')

    """
    Turn the robot in a cardinal direction.
    
    Direction must be one of N, S, E or W.
    """
    def turn(self, direction: str):
        return post('/turn/' + direction)

    """
    Move the robot in the direction in which it is faces.
    """
    def move(self):
        return post('/move')

    """
    Scan area
    """
    def scan(self):
        return post('/scanArea')

    """
    Collects an item previously scanned. Must be located on the item.
    """
    def collect_item(self, id: int):
        return post('/collectItem/' + str(id))

    """
    Unloads the item when the robot is at the the proper disposal bin.
    """
    def unload_item(self, id: int):
        return post('/unloadItem/' + str(id))
