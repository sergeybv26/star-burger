#!/bin/bash
set -e

REPOSITORY=`pwd`

cd "$REPOSITORY"
git status
echo "Fetching"
git fetch
echo "Pulling"
git pull

echo "Up or restart containers"
docker compose up -d --build 

echo "Deploy is completed"
