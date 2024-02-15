import pandas as pd
import kfp
import kfp.components as comp
import kfp.dsl as dsl
from kfp.compiler import Compiler
from google.cloud import storage
from config import PROJECT_ID, SECRET_ID, VERSION_ID, PROJECT_ID, BUCKET_NAME, DATA_FILE_NAME, TARGET_FILE_NAME
from google.cloud import aiplatform
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import io
import logging
from kfp.v2.dsl import component


@component
def download_and_prepare_data(data_file_name: str, target_file_name: str) -> dict:
    # Initialize client
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)

    # Download data
    blob_data = bucket.blob(data_file_name)
    blob_target = bucket.blob(target_file_name)
    content_data = blob_data.download_as_string().decode("utf-8")
    content_target = blob_target.download_as_string().decode("utf-8")

    # Convert CSVs to DataFrame
    df_data = pd.read_csv(io.StringIO(content_data))
    df_target = pd.read_csv(io.StringIO(content_target))

    # Convert DataFrame to numpy arrays
    X = df_data.values
    y = df_target.values.ravel()

    return {"X": X.tolist(), "y": y.tolist()}

@component
def train_model(data: dict) -> float:
    X = pd.DataFrame(data['X'])
    y = pd.Series(data['y'])

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train a RandomForest Classifier
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {accuracy}")

    return accuracy

# Define the pipeline
@dsl.pipeline(
    name="Classification Pipeline",
    description="A pipeline that trains a model on provided dataset"
)
def pipeline(data_file_name: str, target_file_name: str):
    data_output = download_and_prepare_data(data_file_name=data_file_name, target_file_name=target_file_name)
    accuracy = train_model(data=data_output.output)

# Compile the pipeline
kfp.v2.compiler.Compiler().compile(pipeline_func=pipeline, package_path='classification_pipeline.json')

# Specify the values for the pipeline's parameters
data_file_name = DATA_FILE_NAME
target_file_name = TARGET_FILE_NAME

# Run the pipeline
job = aiplatform.PipelineJob(
    display_name="classification-pipeline",
    template_path="classification_pipeline.json",
    pipeline_root=f"gs://{BUCKET_NAME}/pipeline_root",
    parameter_values={'data_file_name': data_file_name, 'target_file_name': target_file_name}
)

try:
    job.run()
except Exception as e:
    logging.exception("Error occurred while running the pipeline job")
    raise e
