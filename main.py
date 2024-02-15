import json
from google.oauth2 import service_account
from google.cloud import secretmanager
from google.cloud import storage
from config import PROJECT_ID, SECRET_ID, VERSION_ID, PROJECT_ID, BUCKET_NAME, DATA_FILE_NAME, TARGET_FILE_NAME
from google.cloud import aiplatform
import pandas as pd
import io

from kfp import dsl
from kfp import compiler
from kfp.dsl import component
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import tempfile
import os


storage_client = storage.Client()
bucket = storage_client.get_bucket(BUCKET_NAME)

# Download data
blob_data = bucket.blob(DATA_FILE_NAME)
blob_target = bucket.blob(TARGET_FILE_NAME)
content_data = blob_data.download_as_string().decode("utf-8")
content_target = blob_target.download_as_string().decode("utf-8")

# Save blob data to temporary files
with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as data_temp_file:
    data_temp_file.write(content_data)
    data_file_path = data_temp_file.name

with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as target_temp_file:
    target_temp_file.write(content_target)
    target_file_path = target_temp_file.name

@component
def train_model_op(data_file_path: str, target_file_path: str):
    # Read data from the file paths
    X = pd.read_csv(data_file_path)
    y = pd.read_csv(target_file_path)

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a simple model (e.g., RandomForestClassifier)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    # Return the accuracy or other relevant metrics
    return accuracy

# Define and run the pipeline
@dsl.pipeline(
    name="model-training-pipeline",
    description="Pipeline for training and evaluating a model."
)
def pipeline(data_file_path: str, target_file_path: str):
    train_model = train_model_op(data_file_path=data_file_path, target_file_path=target_file_path)


# Compile the pipeline
compiler.Compiler().compile(pipeline_func=pipeline, package_path='classification_pipeline.json')

# Run the pipeline
job = aiplatform.PipelineJob(
    display_name="classification-pipeline",
    template_path="classification_pipeline.json",
    pipeline_root=f"gs://{BUCKET_NAME}/pipeline_root",
    parameter_values={'data_file_path': data_file_path, 'target_file_path': target_file_path}
)

from google.auth import default
_, project_id = default()
print(f"Service Account: {project_id}")

job.run()
