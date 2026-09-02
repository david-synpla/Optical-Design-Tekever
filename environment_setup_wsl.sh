#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_ROOT="${HOME}/.local/share/tekever-optiland/venv"

cd "$PROJECT_ROOT"

if ! command -v python3 >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv python3-pip
fi

mkdir -p "$(dirname "$VENV_ROOT")"
if [[ ! -x "$VENV_ROOT/bin/python" ]]; then
    if ! python3 -m venv "$VENV_ROOT"; then
        sudo apt-get update
        sudo apt-get install -y python3-venv
        python3 -m venv "$VENV_ROOT"
    fi
fi

PYTHON="$VENV_ROOT/bin/python"
"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install -r requirements.in

printf '%s\n' "$PYTHON" > python_path.txt
"$PYTHON" -m pip freeze > requirements-lock-wsl.txt
"$PYTHON" src/verify_env.py
"$PYTHON" src/verify_optiland_trace.py

printf '\nEnvironment ready.\nPython: %s\n' "$PYTHON"
