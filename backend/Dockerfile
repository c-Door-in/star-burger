FROM python:3.10-slim-bookworm

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libpq-dev gcc git \
    && apt-get clean

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir /app/static
RUN mkdir /app/staticdiles
