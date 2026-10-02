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

echo Running unit tests...
".venv\Scripts\python.exe" -m pytest tests %*
if %ERRORLEVEL% neq 0 (
    echo.
    echo [TESTS FAILED] Some tests did not pass.
    exit /b %ERRORLEVEL%
) else (
    echo.
    echo [TESTS PASSED] All tests completed successfully!
)
