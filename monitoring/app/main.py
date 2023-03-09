"""Main module."""
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.routers import router
import pickle
import pandas as pd
from entrada import Entrada
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


app = FastAPI(title='Monitoramento de modelos', version="1.0.0")

with open('../model.pkl', 'rb') as f:
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
    entrada = entrada.dict()

    df = pd.DataFrame([entrada], columns=entrada.keys())
    df = df.drop(columns=['TARGET'], axis=1)

    yhat = model.predict(df)[0]

    return {"predicao": int(yhat)}

app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
