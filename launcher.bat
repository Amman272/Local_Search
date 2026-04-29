@echo off
echo Starting Local File Search...

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python to run this application.
    pause
    exit /b
)

:: Check and install requirements quietly
echo Checking dependencies (this might take a moment on first run)...
python -m pip install -r requirements.txt -q

:: Run the desktop app
python desktop_app.py
