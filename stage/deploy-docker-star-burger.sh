#!/usr/bin/bash

set -e

sudo -v

sudo docker compose up -d --build

sudo systemctl reload nginx.service

echo "Deploy complete"
