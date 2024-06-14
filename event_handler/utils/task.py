import asyncio
import httpx
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from event_handler.services.storageAccount import AzureBlobStorage
from event_handler.configs.secrets import STORAGGEACCOUNT, API_HOST, API_PORT

azure_storage = AzureBlobStorage(STORAGGEACCOUNT)

async def create_container_and_folders():
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    container_name = f"container-{current_time}"
    azure_storage.create_container_with_folders(container_name)

async def make_post_requests():
    try:
        async with httpx.AsyncClient() as client:
            response1 = await client.post(f"http://{API_HOST}:{API_PORT}/first-endpoint")
            logging.info(f"First POST response: {response1.json()}")
            response2 = await client.post(f"http://{API_HOST}:{API_PORT}/second-endpoint")
            logging.info(f"Second POST response: {response2.json()}")
            if response1.status_code == 200 and response2.status_code == 200:
                response3 = await client.post(f"http://{API_HOST}:{API_PORT}/third-endpoint")
                logging.info(f"Third POST response: {response3.json()}")
    except Exception as e:
        logging.error(f"Error during POST requests: {e}")

async def scheduled_task():
    #await create_container_and_folders()
    await make_post_requests()

def scheduled_task_wrapper():
    asyncio.run(scheduled_task())

def schedule_daily_task():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_task_wrapper, 'interval', seconds=5)
    scheduler.start()
