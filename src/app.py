from fastapi import FastAPI
import uvicorn

from src.logger import LOGGER
from src.middleware.requests import log_requests
from src.utils.task import schedule_daily_task

from src.router import health_check, trigger

from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run before the app starts
    logging.info("Starting up application")
    schedule_daily_task()
    yield
    # Code to run after the app is shut down
    logging.info("Shutting down application")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.middleware("http")(log_requests)

app.include_router(health_check.router, tags=["health"])
app.include_router(trigger.router)

