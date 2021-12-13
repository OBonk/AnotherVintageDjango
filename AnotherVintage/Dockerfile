# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
ENV MONGO_INITDB_ROOT_USERNAME root
ENV MONGO_INITDB_ROOT_PASSWORD rootpassword
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/