FROM node:18-bookworm

WORKDIR /usr/src/app

RUN apt-get update

COPY package*.json ./

# COPY package-lock.json ./

RUN npm ci --include=dev && npm cache clean --force

# COPY . .

# RUN ./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
