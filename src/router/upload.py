from fastapi import APIRouter, UploadFile,HTTPException, File
from fastapi.responses import FileResponse
from src.services.storageAccount import AzureBlobStorage
from datetime import datetime
import os
import zipfile
import shutil
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


@router.get("/download-container/")
async def download_container(container_name: str):
    current_time = datetime.now().strftime("%Y-%m-%d")
    if container_name != current_time:
        raise HTTPException(status_code=400, detail=f"Invalid container name. Must be today's date in format YYYY-MM-DD. Today's date is {current_time}.")

    if not await blob_storage.container_exists(container_name):
        raise HTTPException(status_code=400, detail="Container does not exist. Please provide a valid container name.")

    # Diretório temporário para armazenar blobs
    temp_dir = f"temp_{container_name}"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Lista de blobs no container
        blobs = blob_storage.list_blobs(container_name)

        # Baixa cada blob e salva no diretório temporário
        for blob_name in blobs:
            download_path = os.path.join(temp_dir, blob_name)
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            blob_storage.download_blob(container_name, blob_name, download_path)

        # Compacta todos os arquivos em um único arquivo ZIP
        zip_filename = f"{container_name}.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, temp_dir))

        # Retorna o arquivo ZIP para download
        return FileResponse(zip_filename, media_type='application/zip', filename=zip_filename)
    finally:
        # Remove o diretório temporário e o arquivo ZIP após a resposta
        shutil.rmtree(temp_dir)
        if os.path.exists(zip_filename):
            os.remove(zip_filename)