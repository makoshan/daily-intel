@echo off
REM Daily Intel - Run Pipeline Script for Windows

echo ========================================
echo Daily Intel - Running Pipeline
echo ========================================
echo.

cd /d "%~dp0"

REM Check if .env exists
if not exist "scripts\.env" (
    echo ERROR: scripts\.env file not found!
    echo Please run install.bat first and configure your API key
    pause
    exit /b 1
)

echo Starting pipeline...
echo.

python scripts\daily-intel-pipeline-enhanced.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo Pipeline failed with errors
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo Pipeline completed successfully!
echo ========================================
echo.
echo Generated files are in: _posts\
echo.
echo To preview locally:
echo   bundle exec jekyll serve
echo.
pause
