@echo off
setlocal enabledelayedexpansion

echo =========================================
echo      Local File Search - Installer
echo =========================================

:: Define target folder name
set "APP_DIR=Local_Search_App"

:: 1. Check if folder already exists
if exist "%APP_DIR%" (
    echo [INFO] Application already downloaded.
    goto :run_app
)

echo [INFO] Downloading the latest version from GitHub...
curl -L -o repo.zip https://github.com/Amman272/Local_Search/archive/refs/heads/main.zip
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to download the application. Please check your internet connection.
    pause
    exit /b
)

echo [INFO] Extracting files...
tar -xf repo.zip
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to extract the application.
    pause
    exit /b
)

:: Rename the extracted GitHub folder
move Local_Search-main "%APP_DIR%" >nul
del repo.zip

:run_app
cd "%APP_DIR%"

:: 2. Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed. Please install Python to run this application.
    pause
    exit /b
)

:: 3. Install Requirements
echo [INFO] Checking and installing required dependencies (this may take a moment)...
python -m pip install -r requirements.txt -q

:: Install Pywebview independently (graceful fail)
echo [INFO] Setting up native window support...
python -m pip install pywebview -q >nul 2>&1

:: Create Desktop Shortcut
if exist "create_shortcut.bat" (
    call create_shortcut.bat
) else (
    echo [WARNING] create_shortcut.bat not found. Skipping shortcut creation.
)

:: 4. Run the desktop app
echo [INFO] Launching Application...
python desktop_app.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Application crashed!
    pause
)
pause
