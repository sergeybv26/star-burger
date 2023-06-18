#!/bin/bash
set -e

REPOSITORY=`pwd`

cd "$REPOSITORY"
git status
echo "Fetching"
git fetch
echo "Pulling"
git pull

echo "Restart containers"
docker compose restart

echo "Deploy is completed"
