# Creating a venv Environment for Scripts and Jupyter Notebooks
python3.9 -m venv venv

## Activating the Environment
source venv/bin/activate

## Installing the Requirements
pip install -r requirements.txt

## Commands
python main.py

### Build image
docker build -t production_image .

### Create container
docker run --name production_container production_image

docker run --name production_container -v /home/jhoeel/gcp/cloud_storage/storage_secret/keys.json:/key.json -e GOOGLE_APPLICATION_CREDENTIALS=/key.json production_image

docker run -it --entrypoint /bin/bash --name production_container -v /home/jhoeel/gcp/cloud_storage/storage_secret/keys.json:/key.json -e GOOGLE_APPLICATION_CREDENTIALS=/key.json production_image

### Remove container and image
docker container prune -f && docker rmi production_image