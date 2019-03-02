import requests

BASE = 'https://someurl.com'

def get(url):
    return requests.get(BASE + url)

def some_endpoint():
    return get('/some_endpoint')
