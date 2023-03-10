"""Main module."""
import json
import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import validate_model
from api.routers import router
import pickle
import pandas as pd
from entrada import Entrada
from fastapi.responses import JSONResponse


app = FastAPI(title='Monitoramento de modelos', version="1.0.0")

with open('monitoring/model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.get("/")
def read_root():
    """Hello World message."""
    return {"Hello World": "from FastAPI"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.post("/predict")
def prediction_test(entrada: Entrada):
    """
    Função que retorna uma predição, dado que uma entrada no formato
    definido por Entrada em entrada.py foi fornecido. Os resultados podem
    ser 0 ou 1.
    """
    try:
        entrada = entrada.dict()
        validate_model(Entrada, entrada)
        try:
            df = pd.DataFrame([entrada], columns=entrada.keys())
            df = df.drop(columns=['TARGET'], axis=1)

            yhat = model.predict(df)[0]

            return {"predicao": int(yhat)}
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail='Invalid JSON object provided'
        ) 

app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
