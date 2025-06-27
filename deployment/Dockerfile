FROM python:3.9-slim

RUN pip install kafka-python boto3 requests

WORKDIR /app
COPY . .

CMD ["python", "script.py"]

