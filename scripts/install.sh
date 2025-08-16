#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV="${VENV:-.venv}"

if [[ ! -d "$VENV" ]]; then
  "$PYTHON_BIN" -m venv "$VENV"
fi

"$VENV/bin/pip" install -U pip
"$VENV/bin/pip" install -r requirements.txt

# ensure .env exists
[[ -f .env ]] || cp .env.example .env

echo "✅ install complete (venv: $VENV)"
