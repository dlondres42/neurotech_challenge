"""Endpoint para cálculo de aderência."""
from urllib.request import Request
from fastapi import APIRouter

router = APIRouter(prefix="/aderencia")

@router.post('/ad_calc')
async def calculate_adherence(entrada: str):
    return {'hello': 'world'}