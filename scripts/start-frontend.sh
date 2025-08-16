#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
API_HOST="${HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8010}"
UI_PORT="${UI_PORT:-8510}"
VENV="${VENV:-.venv}"
API_URL="http://$API_HOST:$API_PORT" "$VENV/bin/streamlit" run frontend/app.py --server.address "$API_HOST" --server.port "$UI_PORT"
