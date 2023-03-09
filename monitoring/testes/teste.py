import requests


base = 'http://127.0.0.1:8000/'
headers = {'Content-Type': 'application/json; charset=utf-8'}

def test_invalid_request():
    url = base + '/v1/performance'
    body = {'sources': [{'twitter': True, 'sisouv': True,'google': True}]}
    response = requests.post(url, json=body)

    assert response.apparent_encoding == 'json'
    assert response.status_code == 400