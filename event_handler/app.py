from fastapi import FastAPI
import uvicorn

from event_handler.logger import LOGGER
from event_handler.middleware.requests import log_requests
from event_handler.utils.task import schedule_daily_task

from event_handler.router import health_check

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


