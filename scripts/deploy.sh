#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MPREMOTE="$ROOT_DIR/.venv/bin/mpremote"
PORT="${1:-${ESP32_PORT:-}}"

if [[ ! -x "$MPREMOTE" ]]; then
  echo "mpremote not found at $MPREMOTE"
  echo "Activate the virtual environment and install dependencies first."
  exit 1
fi

if [[ -z "$PORT" ]]; then
  for candidate in /dev/cu.usbmodem* /dev/cu.usbserial* /dev/ttyUSB* /dev/ttyACM*; do
    [[ -e "$candidate" ]] || continue
    if "$MPREMOTE" connect "$candidate" exec "import sys; print(sys.implementation.name)" >/dev/null 2>&1; then
      PORT="$candidate"
      break
    fi
  done
fi

if [[ -z "$PORT" ]]; then
  echo "No MicroPython ESP32 board detected."
  echo "Connect the board and rerun, or pass a port explicitly: ./scripts/deploy.sh /dev/cu.usbmodem101"
  exit 1
fi

echo "Using port: $PORT"
"$MPREMOTE" connect "$PORT" fs cp "$ROOT_DIR/boot.py" :boot.py
"$MPREMOTE" connect "$PORT" fs cp "$ROOT_DIR/main.py" :main.py
"$MPREMOTE" connect "$PORT" fs cp "$ROOT_DIR/index.html" :index.html
"$MPREMOTE" connect "$PORT" fs cp "$ROOT_DIR/credentials.py" :credentials.py
"$MPREMOTE" connect "$PORT" reset

echo "Deployment complete. Board reset on $PORT"
