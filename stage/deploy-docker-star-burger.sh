#!/usr/bin/bash

set -e

sudo -v

cd ../

/usr/bin/git pull

cd stage

sudo docker compose up --build 

sudo systemctl reload nginx.service

echo "Deploy complete"
