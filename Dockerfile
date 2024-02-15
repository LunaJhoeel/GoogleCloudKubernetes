# Use python:3.9-slim-buster as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install additional dependencies for the Google Cloud SDK
RUN apt-get update && apt-get install -y curl gnupg

# Add the Cloud SDK distribution URI as a package source
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install the Google Cloud SDK
RUN apt-get update && apt-get install -y google-cloud-sdk

# Copy the requirements.txt file and install Python dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code to the container
COPY . /app

# Set environment variable for Google application credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=keys.json

# Run the secret manager script
#RUN python secret_manager.py

# Set environment variable for Google application credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=full_access.json

# Debug: Show the contents of the service account file
RUN cat $GOOGLE_APPLICATION_CREDENTIALS

# Activate the service account with the new credentials
RUN gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

# Set the default command for the container
CMD ["python", "main.py"]
