@echo off
title Mobile Proto Generator for Proxy
color 0b

echo ==================================================
echo        MOBILE PROTO GENERATOR FOR PROXY
echo ==================================================
echo  Checking system environment...
echo ==================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Python is not installed or not added to your system PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b
)

echo [✓] Python is installed.
echo.

:: Ask user what they want to do
:menu
echo Choose an option:
echo [1] Generate a single fresh mobile proto (Hex only)
echo [2] Generate and show full details (Model, Brand, IMEI, etc.)
echo [3] Generate and save 5 protos to a file (generated_protos.json)
echo [4] Generate and upload a proto directly to Firebase
echo [5] Exit
echo.

set /p choice="Enter option (1-5): "

if "%choice%"=="1" (
    echo.
    python main.py
    echo.
    pause
    goto menu
)
if "%choice%"=="2" (
    echo.
    python main.py --details
    echo.
    pause
    goto menu
)
if "%choice%"=="3" (
    echo.
    python main.py --count 5 --output generated_protos.json
    echo.
    pause
    goto menu
)
if "%choice%"=="4" (
    echo.
    echo Make sure you have set the FIREBASE_URL environment variable if using a custom database.
    python main.py --count 1 --upload
    echo.
    pause
    goto menu
)
if "%choice%"=="5" (
    exit /b
)

echo Invalid choice. Please try again.
echo.
goto menu
