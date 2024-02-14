from secret_manager import access_secret_version
from storage_manager import read_file
from config import PROJECT_ID, SECRET_ID, VERSION_ID, BUCKET_NAME, FILE_NAME

if __name__ == "__main__":
    secret_content = access_secret_version(PROJECT_ID, SECRET_ID, VERSION_ID)
    read_file(secret_content, BUCKET_NAME, FILE_NAME)