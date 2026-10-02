#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "======================================================="
echo "   Typing Trainer - Build Standalone Executable"
echo "======================================================="

if [ ! -f ".venv/bin/python" ]; then
    echo "Virtual environment not found. Setting up environment first..."
    chmod +x ./setup_env.sh
    ./setup_env.sh
fi

# 1. Compile translations
echo "[1/2] Compiling localization files..."
if [ -f "scripts/compile_locales.py" ]; then
    .venv/bin/python scripts/compile_locales.py
fi

# 2. Run cx_Freeze build
echo "[2/2] Building executable with cx_Freeze..."
.venv/bin/python setup.py build "$@"

echo ""
echo "======================================================="
echo "   Build completed successfully!"
echo "   Output directory: dist/TypingTrainer"
echo "======================================================="
echo ""
