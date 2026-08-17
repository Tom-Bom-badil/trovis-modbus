#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"

cd "$ROOT_DIR"

if ! "$PYTHON_BIN" -c "import modbus_connection" >/dev/null 2>&1; then
    echo "==> Installing project dependencies"
    "$PYTHON_BIN" -m pip install \
        --root-user-action=ignore \
        -e .
fi

if ! "$PYTHON_BIN" -c "import pytest, pytest_asyncio" >/dev/null 2>&1; then
    echo "==> Installing test dependencies"
    "$PYTHON_BIN" -m pip install \
        --root-user-action=ignore \
        "pytest>=8" \
        "pytest-asyncio>=0.24"
fi

export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

exec "$PYTHON_BIN" -m pytest "$@"
