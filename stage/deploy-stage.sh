#!/usr/bin/bash

set -e

sudo -v

sudo mkdir -p /var/www/docker-star-burger-site
sudo mkdir -p /var/www/docker-star-burger-site/staticfiles

sudo docker compose up

sudo systemctl reload nginx.service

echo "Deploy complete"
