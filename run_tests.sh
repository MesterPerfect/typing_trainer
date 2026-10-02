#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -f ".venv/bin/python" ]; then
    echo "Virtual environment not found. Setting up environment first..."
    chmod +x ./setup_env.sh
    ./setup_env.sh
fi

echo "Running unit tests..."
exec .venv/bin/python -m pytest tests/ "$@"
