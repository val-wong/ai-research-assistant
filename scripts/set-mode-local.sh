#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
[[ -f .env ]] || cp .env.example .env
python3 - "$@" <<'PY'
import re, pathlib
p=pathlib.Path('.env'); s=p.read_text()
def setkv(s,k,v):
    return re.sub(rf'^{k}=.*$', f'{k}={v}', s, flags=re.M) if re.search(rf'^{k}=', s, flags=re.M) else s+f'\n{k}={v}\n'
s=setkv(s,'USE_OPENAI','false')
s=setkv(s,'EMBED_MODEL','all-MiniLM-L6-v2')
p.write_text(s)
print("✅ Mode set to LOCAL (no OpenAI calls).")
PY
