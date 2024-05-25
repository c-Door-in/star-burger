#!/usr/bin/bash

set -e

sudo -v

sudo mkdir -p /var/www/docker-star-burger-site
sudo mkdir -p /var/www/docker-star-burger-site/staticfiles

cd ../backend
docker build --tag star-burger-backend .

cd ../frontend
docker build --tag star-burger-frontend .

cd ../stage
sudo docker compose up

sudo systemctl reload nginx.service

echo "Deploy complete"
