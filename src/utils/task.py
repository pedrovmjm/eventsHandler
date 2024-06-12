import asyncio
import httpx
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.services.storageAccount import AzureBlobStorage
from src.configs.secrets import STORAGGEACCOUNT

connection_string = STORAGGEACCOUNT
azure_storage = AzureBlobStorage(connection_string)

async def create_container_and_folders():
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    container_name = f"container_{current_time}"
    azure_storage.create_container_with_folders(container_name)

async def make_post_requests():
    try:
        async with httpx.AsyncClient() as client:
            response1 = await client.post("http://127.0.0.1:8000/first-endpoint")
            logging.info(f"First POST response: {response1.json()}")
            response2 = await client.post("http://127.0.0.1:8000/second-endpoint")
            logging.info(f"Second POST response: {response2.json()}")
            if response1.status_code == 200 and response2.status_code == 200:
                response3 = await client.post("http://127.0.0.1:8000/third-endpoint")
                logging.info(f"Third POST response: {response3.json()}")
    except Exception as e:
        logging.error(f"Error during POST requests: {e}")

async def scheduled_task():
    await create_container_and_folders()
    await make_post_requests()

def scheduled_task_wrapper():
    asyncio.run(scheduled_task())

def schedule_daily_task():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_task_wrapper, 'interval', seconds=30)
    scheduler.start()
