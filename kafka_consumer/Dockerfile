# Dockerfile for Kafka Consumer
FROM python:3.11 

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# The source code will be mounted as a volume
