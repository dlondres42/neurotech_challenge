import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from http import client
from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)

"""
    Este arquivo serve para testar o endpoint do calculo da aderencia
"""


filepath_train = "/Users/davidubaldo/Neuro/challenge-data-scientist/datasets/credit_01/train.gz"
filepath_oot = "/Users/davidubaldo/Neuro/challenge-data-scientist/datasets/credit_01/oot.gz"

# Test using train.gz's filepath as input
def test_correct_adherence_train():
    response = client.post("/v1/aderencia/ad_calc", params={'filepath': filepath_train})
    assert response.status_code == 200
    assert response.json() == {"distance":0.002759858953621075}

# Test using oot.gz's filepath as input
def test_correct_adherence_oot():
    response = client.post("/v1/aderencia/ad_calc", params={'filepath': filepath_oot})
    assert response.status_code == 200
    assert response.json() == {"distance":0.020915414151451373}