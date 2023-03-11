"""Endpoint para cálculo de aderência."""
import json
import pickle
from fastapi import APIRouter, HTTPException, status
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

router = APIRouter(prefix="/aderencia")

with open('monitoring/model.pkl', 'rb') as f:
    model = pickle.load(f)

test = pd.read_csv('datasets/credit_01/test.gz', compression='gzip', header=0, sep=',', low_memory=False)

"""
Quando testei o cálculo da aderencia no dataset oot.gz, foi encontrada
uma variável que não estava presente no dataset de treino, impossibilitando
o funcionamento do modelo. A função abaixo é uma solução ingênua para o problema,
onde eu pego todas as categorias do dataset de teste que não estavam presentes 
no dataset de treino  e substituo por np.nan. O ideal seria resolver de outra forma
mais eficiente, com uma solução que demorasse menos para executar.
"""
def preprocess_input(input: pd.DataFrame, model) -> pd.DataFrame:
    for var, cat in zip(model[0].transformers_[1][1].feature_names_in_, model[0].transformers_[1][1][1].categories_):
        input[var] = input[var].apply(lambda x: np.nan if x not in cat else x)

    return input

@router.post('/ad_calc')
async def calculate_adherence(filepath: str):
    try:
        print(f"Received file path: {filepath}")
        try:
            train = pd.read_csv(filepath, compression='gzip', header=0, sep=',', engine='python')
        except FileNotFoundError:
            return {'error': 'File not found'}

        try:
            train = preprocess_input(train, model)
            result = ks_2samp(model.predict_proba(train)[:, 1], model.predict_proba(test)[:, 1])[0] 
            return {'distance': result}

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail='Invalid JSON object provided'
        ) 