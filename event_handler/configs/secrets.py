import os
from dotenv import load_dotenv

load_dotenv()


STORAGGEACCOUNT= os.getenv("STORAGGEACCOUNT")
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')