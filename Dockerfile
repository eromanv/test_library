# Используем базовый образ Python
FROM python:3.9-alpine3.16

ENV PYTHONUNBUFFERED 1

COPY library/requirements.txt /temp/requirements.txt
COPY . /library
WORKDIR /library
EXPOSE 8000
RUN pip install -r /temp/requirements.txt