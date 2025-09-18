#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PROJECT_NAME="openf1-strategy"

echo "⏹ Stopping project containers..."
docker compose -p $PROJECT_NAME -f docker-compose.yml down -v

# If you also have infra/docker-compose.kafka.yml
if [ -f infra/docker-compose.kafka.yml ]; then
  docker compose -p $PROJECT_NAME -f infra/docker-compose.kafka.yml down -v
fi

echo "✅ Project-specific Docker containers, networks, and volumes removed."
