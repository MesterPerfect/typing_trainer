@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo =======================================================
echo   Typing Trainer - Build Executable ^& Installer [Windows]
echo =======================================================

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Setting up environment first...
    call setup_env.bat
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Environment setup failed.
        pause
        exit /b %ERRORLEVEL%
    )
)

REM 1. Compile locales
echo [1/3] Compiling translation files...
if exist "scripts\compile_locales.py" (
    ".venv\Scripts\python.exe" scripts\compile_locales.py
)

REM 2. Build standalone executable using cx_Freeze
echo [2/3] Building executable with cx_Freeze...
".venv\Scripts\python.exe" setup.py build %*
if %ERRORLEVEL% neq 0 (
    echo [ERROR] cx_Freeze build failed.
    pause
    exit /b %ERRORLEVEL%
)

REM 3. Build Inno Setup installer if ISCC is installed
echo [3/3] Checking for Inno Setup Compiler [ISCC]...

set "ISCC_PATH="
where iscc >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "ISCC_PATH=iscc"
) else if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
)

if defined ISCC_PATH (
    echo Compiling Windows Installer with Inno Setup...
    "!ISCC_PATH!" "typingtrainer_setup.iss"
    if !ERRORLEVEL! equ 0 (
        echo [SUCCESS] Windows Installer created in build_installer folder!
    ) else (
        echo [WARNING] Inno Setup compilation had issues.
    )
) else (
    echo [INFO] Inno Setup compiler [ISCC] not found in PATH or standard Program Files.
    echo Standalone executable build is available in: dist\TypingTrainer\
)

echo.
echo =======================================================
echo   Build process completed!
echo   Output directory: dist\TypingTrainer
echo =======================================================
echo.
pause
