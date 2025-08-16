#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
API_HOST="${HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8010}"
VENV="${VENV:-.venv}"
mkdir -p .pids
"$VENV/bin/uvicorn" backend.main:app --host "$API_HOST" --port "$API_PORT" --reload
