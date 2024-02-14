# Creating a venv Environment for Scripts and Jupyter Notebooks
python3.9 -m venv venv

## Activating the Environment
source venv/bin/activate

## Installing the Requirements
pip install -r requirements.txt

## Commands
python main.py

### Build image
docker build -t scrt_image .

### Create container
docker run --name scrt_container scrt_image

### Remove container
docker container prune -f

### Remove image
docker rmi scrt_image


gcloud auth activate-service-account --key-file=/home/jhoeel/gcp/cloud_storage/storage_secret/secrets/pruductiv-1604a8e42e51.json