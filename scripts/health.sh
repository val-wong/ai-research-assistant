#!/usr/bin/env bash
set -euo pipefail
API_HOST="${HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8010}"
curl -s "http://$API_HOST:$API_PORT/healthz" || true
echo
