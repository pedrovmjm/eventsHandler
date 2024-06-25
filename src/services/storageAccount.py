from azure.storage.blob import BlobServiceClient, ContainerClient
import logging
import aiofiles
from fastapi import UploadFile, HTTPException
import os 


class AzureBlobStorage:
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def create_container_with_folders(self, container_name):
        try:
            container_client = self.blob_service_client.create_container(container_name)
            folders = ['ground_truth', 'logs', 'metadata', 'model_output', 'report', 'template', 'transcriptions/txt', 'transcriptions/json', "input/mp3s", "input/metadados"]
            for folder in folders:
                blob_client = container_client.get_blob_client(blob=f"{folder}/")
                blob_client.upload_blob('', overwrite=True)
            logging.info(f"Container and folders created successfully: {container_name}")
        except Exception as e:
            logging.error(f"Error creating container and folders: {e}")

    def list_blobs(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]

    def download_blob(self, container_name, blob_name, download_file_path):
        blob_client = self.blob_service_client.get_blob_client(container_name, blob_name)
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
            
    async def upload_blob(self, container_name, folder_path, blob_name, file: UploadFile):
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob=f"{folder_path}/{blob_name}")

            async with aiofiles.open(file.filename, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            async with aiofiles.open(file.filename, 'rb') as data:
                await blob_client.upload_blob(data, overwrite=True)
            
            os.remove(file.filename)
            logging.info(f"File {blob_name} uploaded to container {container_name} successfully.")
        except Exception as e:
            logging.error(f"Error uploading file to blob storage: {e}")
            raise HTTPException(status_code=500, detail="Error uploading file to blob storage")

    async def container_exists(self, container_name):
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            return await container_client.exists()
        except Exception as e:
            logging.error(f"Error checking if container exists: {e}")
            return False