import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from http import client
from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)

"""
    Este arquivo serve para testar o endpoint do calculo da performanmce
"""

with open("monitoring/batch_records.json", "r") as f:
    test_data = json.load(f)

def test_correct_performance():
    response = client.post("/v1/performance/perf_calc", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"volumetry":{"July":74,"August":72,"May":67,"June":63,"March":62,"January":58,"February":55,"April":49},"auc_roc":0.5751748251748252}


def test_invalid_list_input():
    response = client.post('/v1/performance/perf_calc', json='{"invalid": "json"}')
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
            "loc": [
                "body"
            ],
            "msg": "value is not a valid list",
            "type": "type_error.list"
            }
    ]
}
 
