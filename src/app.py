from fastapi import FastAPI

from src.logger import LOGGER
from src.middleware.requests import log_requests

from src.router import health_check

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.middleware("http")(log_requests)

app.include_router(health_check.router, tags=["health"])

