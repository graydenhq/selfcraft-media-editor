#!/usr/bin/env bash
set -euo pipefail

# Development helper: activate venv and run uvicorn with reload
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT_DIR/.venv"

if [ ! -d "$VENV" ]; then
  echo "Virtualenv not found at $VENV"
  echo "Create it by running: python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

echo "Activating venv and starting uvicorn (dev reload)"
. "$VENV/bin/activate"
python -m uvicorn app.core.main:app --reload --host 127.0.0.1 --port 8000
