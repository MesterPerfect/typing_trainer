@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Setting up environment first...
    call setup_env.bat
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Environment setup failed.
        pause
        exit /b %ERRORLEVEL%
    )
)

REM Ensure translations are compiled
if not exist "locales\ar\LC_MESSAGES\messages.mo" (
    if exist "scripts\compile_locales.py" (
        ".venv\Scripts\python.exe" scripts\compile_locales.py
    )
)

".venv\Scripts\python.exe" main.py %*
