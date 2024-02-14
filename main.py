from google.cloud import storage

def read_file(bucket_name: str, file_name: str):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_string().decode("utf-8")
    print(f"Contenido del archivo '{file_name}':\n{content}")
    return content

if __name__ == "__main__":
    read_file("jhoeel_iris_bucket", "iris_data.csv")
