import requests

BASE = 'http://cec2019.ca'
API_TOKEN = 'brunswick-8Nq9JsYFUtFzdReih3P8s2YMQiRQHDRMkWNkASN5A8xMGa4yzq5njUv4hFEEaBbZ'

def get(url):
    return requests.get(BASE + url, headers={'token': API_TOKEN})

def some_endpoint():
    return get('/some_endpoint')
