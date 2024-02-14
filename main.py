from google.cloud import storage, secretmanager
from google.oauth2 import service_account
import json

def access_secret_version(project_id, secret_id, version_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def read_file(credentials_json, bucket_name, file_name):
    credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_string().decode("utf-8")
    print(f"Contenido del archivo '{file_name}':\n{content}")
    return content

if __name__ == "__main__":
    
    # Replace these variables with your project's values
    project_id = "853577049619"
    secret_id = "secret_name"
    version_id = "latest"
    
    # Retrieve the secret (e.g., your 'GOOGLE_APPLICATION_CREDENTIALS' JSON)
    secret_content = access_secret_version(project_id, secret_id, version_id)
    
    read_file(secret_content, "jhoeel_iris_bucket", "iris_data.csv")
