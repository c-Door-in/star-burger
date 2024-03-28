FROM node:16-bookworm AS frontender

WORKDIR /app

RUN apt-get update \
    && apt-get clean

COPY . .

RUN npm install --include=dev && npm cache clean --force
