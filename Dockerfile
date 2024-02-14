FROM python:3.9-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/pruductiv-1604a8e42e51.json

CMD ["python", "main.py"]
