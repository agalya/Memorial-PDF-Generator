@echo off
REM Start Memorial PDF Generator Web Server
REM This script installs dependencies and launches the Flask app

echo.
echo ===================================
echo Memorial PDF Generator - Web Server
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✓ Dependencies installed
echo.
echo Starting web server...
echo.
echo Open your browser and go to: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the Flask app
python app.py
