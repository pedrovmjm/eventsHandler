from pydantic import BaseModel
from fastapi import APIRouter
from src.models.health_check import HealthCheck

router = APIRouter()

@router.get("health",
            response_model=HealthCheck)
def health_check():
    return {"stauts": "OK"}