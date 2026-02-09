@echo off
REM Daily Intel - Installation Script for Windows

echo ========================================
echo Daily Intel - Installing Dependencies
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/3] Installing required packages...
pip install -r scripts\requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [3/3] Creating .env file...
if not exist "scripts\.env" (
    copy "scripts\.env.example" "scripts\.env"
    echo.
    echo IMPORTANT: Please edit scripts\.env and add your OPENAI_API_KEY
    echo.
) else (
    echo .env file already exists, skipping...
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit scripts\.env and add your OpenAI API Key
echo 2. Run: run-pipeline.bat
echo.
pause
