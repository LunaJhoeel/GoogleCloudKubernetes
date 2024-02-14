from google.cloud import storage
from google.oauth2 import service_account
import json

def read_file(credentials_json, bucket_name, file_name):
    credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_string().decode("utf-8")
    print(f"Contenido del archivo '{file_name}':\n{content}")
    return content

