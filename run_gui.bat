@echo off
title YT-DLP GUI Launcher
echo Starting YT-DLP GUI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if yt-dlp is installed
python -c "import yt_dlp" >nul 2>&1
if %errorlevel% neq 0 (
    echo yt-dlp is not installed. Installing now...
    pip install yt-dlp
    if %errorlevel% neq 0 (
        echo Error: Failed to install yt-dlp
        pause
        exit /b 1
    )
)

REM Run the GUI
python yt_dlp_gui.py
if %errorlevel% neq 0 (
    echo Error: Failed to start GUI
    pause
    exit /b 1
)

echo.
echo GUI closed successfully
pause
