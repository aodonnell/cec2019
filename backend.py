import abc

import requests

BASE = 'http://cec2019.ca'
API_TOKEN = 'brunswick-8Nq9JsYFUtFzdReih3P8s2YMQiRQHDRMkWNkASN5A8xMGa4yzq5njUv4hFEEaBbZ'


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


# Request Wrappers for Attaching API Token
def get(url):
    return requests.get(BASE + url, headers={'token': API_TOKEN})


def delete(url):
    return requests.delete(BASE + url, headers={'token': API_TOKEN})


def post(url):
    return requests.post(BASE + url, headers={'token': API_TOKEN})


# noinspection PyMethodMayBeStatic
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
    Delete the current instance
    """
    def delete_instance(self):
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
    def turn(self, direction):
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
    def collect_item(self, id):
        return post('/collectItem/' + id)

    """
    Unloads the item when the robot is at the the proper disposal bin.
    """
    def unload_item(self, id):
        return post('/unloadItem/' + id)
