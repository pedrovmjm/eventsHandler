from fastapi import APIRouter
import logging

router = APIRouter()

@router.post("/first-endpoint")
async def first_endpoint():
    logging.info("First endpoint triggered")
    return {"message": "First endpoint triggered"}

@router.post("/second-endpoint")
async def second_endpoint():
    logging.info("Second endpoint triggered")
    return {"message": "Second endpoint triggered"}

@router.post("/third-endpoint")
async def third_endpoint():
    logging.info("Third endpoint triggered")
    return {"message": "Third endpoint triggered"}
