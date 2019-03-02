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


def get_instance():
    return get('/instance')

def delete_instance():
    return delete('/instance')

def finish():
    return post('/finish')

def turn(direction):
    return post('/turn/' + direction)

def move():
    return post('/move')

def scan():
    return post('/scanArea')

def collect_item(id):
    return post('/collectItem/' + id)

def unload_item(id):
    return post('/unloadItem/' + id)
