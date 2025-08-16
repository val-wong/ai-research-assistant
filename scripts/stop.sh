#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f .pids/backend.pid ]]; then kill "$(cat .pids/backend.pid)" 2>/dev/null || true; fi
if [[ -f .pids/frontend.pid ]]; then kill "$(cat .pids/frontend.pid)" 2>/dev/null || true; fi

pkill -f "uvicorn backend.main:app" 2>/dev/null || true
pkill -f "streamlit run frontend/app.py" 2>/dev/null || true

rm -f .pids/backend.pid .pids/frontend.pid
echo "🧹 Stopped backend & frontend."
