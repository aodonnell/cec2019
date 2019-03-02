import requests

BASE = 'http://cec2019.ca'
API_TOKEN = 'brunswick-8Nq9JsYFUtFzdReih3P8s2YMQiRQHDRMkWNkASN5A8xMGa4yzq5njUv4hFEEaBbZ'

# Request Wrappers for Attaching API Token
def get(url):
    return requests.get(BASE + url, headers={'token': API_TOKEN})

def delete(url):
    return requests.delete(BASE + url, headers={'token': API_TOKEN})

def post(url):
    return requests.post(BASE + url, headers={'token': API_TOKEN})


"""
Create the current instance
"""
def create_instance():
    return post('/instance')

"""
Retrieve the current instance
"""
def get_instance():
    return get('/instance')

"""
Delete the current instance
"""
def delete_instance():
    return delete('/instance')

"""
Declare collection complete
"""
def finish():
    return post('/finish')

"""
Turn the robot in a cardinal direction.

Direction must be one of N, S, E or W.
"""
def turn(direction):
    return post('/turn/' + direction)

"""
Move the robot in the direction in which it is faces.
"""
def move():
    return post('/move')

"""
Scan area
"""
def scan():
    return post('/scanArea')

"""
Collects an item previously scanned. Must be located on the item.
"""
def collect_item(id):
    return post('/collectItem/' + id)

"""
Unloads the item when the robot is at the the proper disposal bin.
"""
def unload_item(id):
    return post('/unloadItem/' + id)
