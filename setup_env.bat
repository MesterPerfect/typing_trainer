@echo off
setlocal enabledelayedexpansion

echo =======================================================
echo   Typing Trainer - Environment Setup [Windows]
echo =======================================================

cd /d "%~dp0"

REM 1. Check Python installation
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not found in your PATH.
    echo Please install Python 3.10+ from https://www.python.org/ and check "Add Python to PATH".
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

REM 2. Create Virtual Environment (.venv)
if not exist ".venv" (
    echo [2/4] Creating virtual environment .venv...
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [2/4] Virtual environment .venv already exists.
)

REM 3. Upgrade pip and install requirements
echo [3/4] Installing and updating dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b 1
)

REM 4. Compile translations
echo [4/4] Compiling localization files...
if exist "scripts\compile_locales.py" (
    ".venv\Scripts\python.exe" scripts\compile_locales.py
)

echo.
echo =======================================================
echo   Environment setup completed successfully!
echo   You can now run:
echo     - run.bat       : To start Typing Trainer
echo     - run_tests.bat : To run unit tests
echo     - build.bat     : To build executable and installer
echo =======================================================
echo.
pause
