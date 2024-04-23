FROM node:16-bookworm AS frontender

WORKDIR /app

RUN apt-get update \
    && apt-get clean

COPY . .

RUN npm install --include=dev && npm cache clean --force

RUN mkdir /app/static
RUN mv ./assets/* ./staticfiles/ -fv

CMD ./node_modules/.bin/parcel build ./bundles-src/index.js --dist-dir ./staticfiles --public-url='./'
