#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

API_HOST="${HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8010}"
UI_PORT="${UI_PORT:-8510}"
VENV="${VENV:-.venv}"
UVICORN="$VENV/bin/uvicorn"
STREAMLIT="$VENV/bin/streamlit"

# Ensure deps/venv and .env
"$SCRIPT_DIR/install.sh" >/dev/null

mkdir -p .pids

# Stop any leftovers
bash "$SCRIPT_DIR/stop.sh" >/dev/null || true

echo "🔌 Starting backend on http://$API_HOST:$API_PORT"
"$UVICORN" backend.main:app --host "$API_HOST" --port "$API_PORT" --reload &
BACK_PID=$!
echo $BACK_PID > .pids/backend.pid

echo "🖥  Starting UI on http://$API_HOST:$UI_PORT  (API → http://$API_HOST:$API_PORT)"
API_URL="http://$API_HOST:$API_PORT" \
"$STREAMLIT" run frontend/app.py --server.address "$API_HOST" --server.port "$UI_PORT" &
FRONT_PID=$!
echo $FRONT_PID > .pids/frontend.pid

trap 'echo; echo "🛑 Stopping..."; bash scripts/stop.sh' INT TERM
wait $BACK_PID $FRONT_PID
