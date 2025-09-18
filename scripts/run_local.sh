#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Step 1: Start Redpanda
echo "🐼 Starting Redpanda..."
docker compose -f infra/docker-compose.kafka.yml up -d redpanda

# Wait until Redpanda is ready
echo "⏳ Waiting for Redpanda to be ready..."
until docker exec redpanda rpk cluster info >/dev/null 2>&1; do
  sleep 2
done
echo "✅ Redpanda is ready."

# Step 2: Ensure .venv exists
if [ ! -d ".venv" ]; then
  echo "❌ .venv not found. Please create and install requirements first."
  exit 1
fi
PYTHON=.venv/bin/python

# Step 3: Start Replay, Engine, API
echo "🚀 Starting Replay, Engine, and API..."

$PYTHON -m ingest.replay > logs_replay.txt 2>&1 &
REPLAY_PID=$!
echo "Replay started (PID $REPLAY_PID)"

$PYTHON -m engine.run > logs_engine.txt 2>&1 &
ENGINE_PID=$!
echo "Engine started (PID $ENGINE_PID)"

$PYTHON -m uvicorn api.main:app --port 8000 > logs_api.txt 2>&1 &
API_PID=$!
echo "API started (PID $API_PID)"

# Trap CTRL+C
trap "echo '⏹ Stopping...'; kill $REPLAY_PID $ENGINE_PID $API_PID; docker compose -f infra/docker-compose.kafka.yml down; exit 0" SIGINT

# Keep script alive
wait
