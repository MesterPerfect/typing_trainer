#!/usr/bin/env bash
set -e

# Change directory to the root of the project
cd "$(dirname "$0")"

echo "======================================================="
echo "   Typing Trainer - Environment Setup (Linux / macOS)"
echo "======================================================="

# 1. Detect Python binary
PYTHON_BIN=""
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "[ERROR] Python 3 was not found on your system."
    echo "Please install Python 3.10 or higher using your package manager (e.g. apt, brew, dnf, pacman)."
    exit 1
fi

echo "[1/4] Found Python: $($PYTHON_BIN --version)"

# 2. Create Virtual Environment (.venv)
if [ ! -d ".venv" ]; then
    echo "[2/4] Creating virtual environment (.venv)..."
    if ! "$PYTHON_BIN" -m venv .venv; then
        echo ""
        echo "[ERROR] Failed to create virtual environment."
        if [ "$(uname -s)" = "Linux" ]; then
            echo "On Debian/Ubuntu, you may need: sudo apt-get install python3-venv python3-pip"
            echo "On Fedora: sudo dnf install python3-devel"
            echo "On Arch Linux: sudo pacman -S python"
        fi
        exit 1
    fi
else
    echo "[2/4] Virtual environment (.venv) already exists."
fi

VENV_PYTHON=".venv/bin/python"
VENV_PIP=".venv/bin/pip"

# 3. Upgrade pip and install requirements
echo "[3/4] Installing / Updating dependencies..."
"$VENV_PYTHON" -m pip install --upgrade pip --quiet
"$VENV_PYTHON" -m pip install -r requirements.txt

# 4. Compile translations
echo "[4/4] Compiling localization files..."
if [ -f "scripts/compile_locales.py" ]; then
    "$VENV_PYTHON" scripts/compile_locales.py
fi

echo ""
echo "======================================================="
echo "   Environment setup completed successfully!"
echo "   You can now run:"
echo "     - ./run.sh       : To start Typing Trainer"
echo "     - ./run_tests.sh : To run unit tests"
echo "     - ./build.sh     : To build standalone binaries"
echo "======================================================="
echo ""
