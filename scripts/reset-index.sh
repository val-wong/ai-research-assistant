#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
API_HOST="${HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8010}"

# Try API endpoint if you added it; else fall back to local wipe.
if curl -fsS -X POST "http://$API_HOST:$API_PORT/reset" >/dev/null 2>&1; then
  echo "✅ Index reset via API."
else
  rm -rf .chroma
  echo "✅ Deleted local .chroma/ (vector store). Re-ingest to rebuild."
fi
