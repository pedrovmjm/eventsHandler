from fastapi import APIRouter, UploadFile,HTTPException, File
from src.services.storageAccount import AzureBlobStorage
from datetime import datetime
from src.configs.secrets import STORAGGEACCOUNT

router = APIRouter()
blob_storage  = AzureBlobStorage(STORAGGEACCOUNT)


@router.post("/upload-mp3/")
async def upload_mp3(container_name: str, file: UploadFile = File(...)):
    current_time = datetime.now().strftime("%Y-%m-%d")
    if container_name != current_time:
        raise HTTPException(status_code=400, detail=f"Invalid container name. Must be today's date in format YYYY-MM-DD. Today's date is {current_time}.")

    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Invalid file type. Only .mp3 files are allowed.")
    
    if file.spool_max_size > 250 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the limit of 250MB.")
    
    if not await blob_storage.container_exists(container_name):
        raise HTTPException(status_code=400, detail="Container does not exist. Please provide a valid container name.")

    await blob_storage.upload_blob(container_name, "input/mp3s", file.filename, file)

    return {"filename": file.filename, "message": "File uploaded successfully."}


@router.post("/upload-json/")
async def upload_json(container_name: str, file: UploadFile = File(...)):
    current_time = datetime.now().strftime("%Y-%m-%d")
    if container_name != current_time:
        raise HTTPException(status_code=400, detail=f"Invalid container name. Must be today's date in format YYYY-MM-DD. Today's date is {current_time}.")

    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid file type. Only .json files are allowed.")
    
    if file.spool_max_size > 250 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the limit of 250MB.")
    
    if not await blob_storage.container_exists(container_name):
        raise HTTPException(status_code=400, detail="Container does not exist. Please provide a valid container name.")

    await blob_storage.upload_blob(container_name, "input/json", file.filename, file)

    return {"filename": file.filename, "message": "File uploaded successfully."}