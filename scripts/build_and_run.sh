#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PROJECT="openf1-strategy"

echo "🧹 Cleaning old containers..."
docker compose -p $PROJECT down -v || true

echo "🔨 Building images..."
docker compose -p $PROJECT build

echo "🚀 Starting full stack..."
docker compose -p $PROJECT up -d

echo "✅ Stack running."
echo "   API:      http://localhost:8000/ping"
echo "   Frontend: http://localhost:5173"
echo "   Kafka UI: use 'docker exec -it redpanda rpk ...'"
