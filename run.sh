#!/usr/bin/env bash
# JARVIS launcher for Mac and Linux.
cd "$(dirname "$0")" || exit 1

PY=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)"; then
    PY="$candidate"
    break
  fi
done
if [ -z "$PY" ]; then
  echo "  Python 3.10 or newer isn't installed yet. Get it free at https://www.python.org/downloads/"
  exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "  First run: setting JARVIS up. This takes about 30 seconds..."
  "$PY" -m venv .venv || { echo "  Couldn't create the Python environment."; exit 1; }
fi

.venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt || {
  echo "  Installing failed. Check your internet connection and run this again."
  exit 1
}

exec .venv/bin/python jarvis.py
