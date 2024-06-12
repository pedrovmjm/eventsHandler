from azure.storage.blob import BlobServiceClient, ContainerClient
import logging


class AzureBlobStorage:
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def create_container_with_folders(self, container_name):
        try:
            container_client = self.blob_service_client.create_container(container_name)
            folders = ['ground_truth', 'logs', 'metadata', 'model_output', 'report', 'template', 'transcriptions/.txt', 'transcriptions/.json']
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
