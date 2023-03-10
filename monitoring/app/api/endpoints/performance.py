"""Endpoint para cálculo de Performance."""
from http import HTTPStatus
import json
from fastapi import APIRouter, HTTPException, status
import numpy as np
from pydantic import validate_model
from entrada import Entrada
from typing import List
import pandas as pd
import pickle
from sklearn.metrics import roc_auc_score
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/performance")

with open('monitoring/model.pkl', 'rb') as f:
    model = pickle.load(f)


def calculate_volumetry(df: pd.DataFrame) -> json:
    month_count = pd.to_datetime(df['REF_DATE'], format='%Y-%m-%d').dt.month_name().value_counts()
    
    return json.loads(json.dumps(month_count.to_dict()))


def calculate_auc(df: pd.DataFrame) -> float:
    x = df.iloc[:, :-1]
    y = df['TARGET']
    yhat = model.predict_proba(x)[:,1]
    auc = roc_auc_score(y, yhat)
    
    return auc


@router.post('/perf_calc')
async def calculate_performance(entradas: List[Entrada]):
    try:
        for entrada in entradas:
            validate_model(Entrada, entrada.dict())

        try: 
            df = pd.DataFrame([entrada.dict() for entrada in entradas])
            df = df.fillna(np.nan)
            volumetry = calculate_volumetry(df)
            auc = calculate_auc(df)

            return JSONResponse(
                content={
                    'volumetry': volumetry,
                    'auc_roc': auc
                },
                status_code=HTTPStatus.OK
        )

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail='Invalid JSON object provided'
        )