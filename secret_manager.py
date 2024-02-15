from google.cloud import secretmanager
from config import PROJECT_ID, SECRET_ID, VERSION_ID
import json

def access_secret_version(project_id, secret_id, version_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def update_keys_file(project_id, secret_id, version_id, file_name='full_access.json'):
    # Fetch secret
    secret_data = access_secret_version(project_id, secret_id, version_id)

    # Convert the secret data to a dictionary
    try:
        secret_data_dict = json.loads(secret_data)
    except json.JSONDecodeError:
        raise ValueError("The fetched secret data is not in valid JSON format")

    # Write the secret data to the specified file (defaults to full_access.json)
    with open(file_name, 'w') as file:
        json.dump(secret_data_dict, file, indent=4)

    # Print success message
    print(f"Successfully updated {file_name} with secret data.")

# Example usage
update_keys_file(PROJECT_ID, SECRET_ID, VERSION_ID)

