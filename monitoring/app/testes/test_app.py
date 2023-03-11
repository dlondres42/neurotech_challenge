import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from http import client
from fastapi.testclient import TestClient
from main import app

"""
Este arquivo visa testar o main.py e o BaseModel entrada, que
é sempre esperado nas requisições post para performance.
"""

client = TestClient(app=app)
input_data = {
    "VAR2": "M",
    "IDADE": 43.893,
    "VAR5": "PR",
    "VAR6": -25.4955709,
    "VAR7": -49.2454987,
    "VAR8": "D",
    "VAR9": "E",
    "VAR10": "MEDIA",
    "VAR11": 1.0,
    "VAR12": 0.182,
    "VAR14": 0.597,
    "VAR15": 0.618,
    "VAR16": 0.25,
    "VAR18": 1.076712,
    "VAR19": 5.057534,
    "VAR22": 0.125,
    "VAR24": 0.069,
    "VAR25": 0.0969999999999999,
    "VAR32": "SALDO INEXISTENTE",
    "VAR39": 0.661039,
    "VAR40": 0.573539,
    "VAR41": 0.4793699999999999,
    "VAR42": 0.4440489999999999,
    "VAR47": 0.006,
    "VAR49": "S",
    "VAR50": "N",
    "VAR51": "N",
    "VAR52": "N",
    "VAR53": "N",
    "VAR54": "N",
    "VAR55": "N",
    "VAR56": "S",
    "VAR57": "S",
    "VAR58": "N",
    "VAR59": "N",
    "VAR60": "N",
    "VAR61": "N",
    "VAR62": "N",
    "VAR63": "N",
    "VAR64": "N",
    "VAR65": "N",
    "VAR66": "ALTISSIMA",
    "VAR67": "ALTA",
    "VAR68": "ALTISSIMA",
    "VAR69": "ALTISSIMA",
    "VAR70": "ALTISSIMA",
    "VAR71": "ALTA",
    "VAR72": "ALTISSIMA",
    "VAR73": "ALTISSIMA",
    "VAR74": "ALTISSIMA",
    "VAR75": "ALTISSIMA",
    "VAR76": "ALTA",
    "VAR77": "ALTISSIMA",
    "VAR78": "ALTISSIMA",
    "VAR79": "ALTISSIMA",
    "VAR80": "ALTA",
    "VAR81": "ALTA",
    "VAR82": "ALTISSIMA",
    "VAR83": "ALTISSIMA",
    "VAR84": "ALTA",
    "VAR85": "ALTA",
    "VAR86": "ALTA",
    "VAR87": "ALTISSIMA",
    "VAR88": "ALTA",
    "VAR89": "ALTISSIMA",
    "VAR90": "BAIXISSIMA",
    "VAR91": "ALTA",
    "VAR92": "ALTISSIMA",
    "VAR93": "ALTISSIMA",
    "VAR94": "ALTISSIMA",
    "VAR95": "ALTA",
    "VAR96": "ALTISSIMA",
    "VAR97": "ALTA",
    "VAR98": "ALTISSIMA",
    "VAR99": "ALTISSIMA",
    "VAR100": "BAIXISSIMA",
    "VAR101": "ALTA",
    "VAR102": "MEDIO",
    "VAR103": "MEDIO",
    "VAR104": "PROXIMO",
    "VAR105": "LONGE",
    "VAR106": "MEDIO",
    "VAR107": "MEDIO",
    "VAR108": "MEDIO",
    "VAR109": "MEDIO",
    "VAR110": "PROXIMO",
    "VAR111": "MEDIO",
    "VAR112": "MEDIO",
    "VAR113": "PROXIMO",
    "VAR114": "PROXIMO",
    "VAR115": "MEDIO",
    "VAR116": "LONGE",
    "VAR117": "MEDIO",
    "VAR118": "MEDIO",
    "VAR119": "LONGE",
    "VAR120": "MUITO LONGE",
    "VAR121": "MEDIO",
    "VAR122": "MEDIO",
    "VAR123": "MEDIO",
    "VAR124": "MEDIO",
    "VAR125": "PROXIMO",
    "VAR126": "MEDIO",
    "VAR127": "PROXIMO",
    "VAR128": "LONGE",
    "VAR129": "MEDIO",
    "VAR130": "MEDIO",
    "VAR131": "MEDIO",
    "VAR132": "PROXIMO",
    "VAR133": "MEDIO",
    "VAR134": "PROXIMO",
    "VAR135": "MEDIO",
    "VAR136": "MEDIO",
    "VAR137": "MEDIO",
    "VAR138": "MEDIO",
    "VAR139": "MEDIO",
    "VAR140": "MUITO PROXIMO",
    "VAR141": 3970.113648,
    "VAR142": "C",
    "REF_DATE": "2017-03-25 00:00:00+00:00",
    "TARGET": 1
}

#testando o main.py
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello World": "from FastAPI"}


def test_correct_prediction():
    response = client.post("/predict", json=input_data)
    assert response.status_code == 200
    assert response.json() == {"predicao": 1}

#testing entrada.py
def test_entrada_date():
    # Testing invalid date as input
    invalid_input = input_data.copy()
    invalid_input['REF_DATE'] = '2023/03/15'
    response = client.post("/predict", json=invalid_input)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "REF_DATE"
                ],
                "msg": "invalid datetime format",
                "type": "value_error.datetime"
            }
        ]
    }

def test_entrada_target():
    # Testing invalid target value as input
    invalid_input = input_data.copy()
    invalid_input['TARGET'] = 10
    response = client.post("/predict", json=invalid_input)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
            "loc": [
                "body",
                "TARGET"
            ],
            "msg": "TARGET must be either 0 or 1",
            "type": "value_error"
            }
        ]
    }


def test_entrada_extra_fields():
    # testing inputing a json with extra fields
    invalid_input = input_data.copy()
    invalid_input['Teste'] = 'Hello'
    response = client.post("/predict", json=invalid_input)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
            "loc": [
                "body",
                "Teste"
            ],
            "msg": "extra fields not permitted",
            "type": "value_error.extra"
            }
    ]
}

def test_entrada_missing_fields():
    # testing inputing a json with missing mandatory fields
    invalid_input = input_data.copy()
    del invalid_input["VAR142"]
    response = client.post("/predict", json=invalid_input)
    assert response.status_code == 500
    assert response.json() == {
  "message": "Found unknown categories [None] in column 98 during transform"
}
    
