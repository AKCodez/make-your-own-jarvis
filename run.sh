#!/usr/bin/env bash
# JARVIS launcher for Mac and Linux.
cd "$(dirname "$0")" || exit 1

for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)"; then
    exec "$candidate" jarvis.py
  fi
done

echo "  Python 3.10 or newer isn't installed yet. Get it free at https://www.python.org/downloads/"
exit 1
