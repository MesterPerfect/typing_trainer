#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -f ".venv/bin/python" ]; then
    echo "Virtual environment not found. Setting up environment first..."
    chmod +x ./setup_env.sh
    ./setup_env.sh
fi

# Ensure translations are compiled
if [ ! -f "locales/ar/LC_MESSAGES/messages.mo" ] && [ -f "scripts/compile_locales.py" ]; then
    .venv/bin/python scripts/compile_locales.py
fi

exec .venv/bin/python main.py "$@"
