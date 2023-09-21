FROM python:3.10-slim-bookworm

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y libpq-dev gcc git \
    && apt-get clean

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# RUN python manage.py migrate

# RUN python manage.py runserver

# CMD [ "python", "manage.py", "runserver", "127.0.0.1:8080" ]