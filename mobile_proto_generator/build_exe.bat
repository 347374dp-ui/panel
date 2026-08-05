@echo off
title Build Mobile Proto Generator Standalone Executable
color 0b

echo ==================================================
echo      BUILD STANDALONE WINDOWS EXECUTABLE
echo ==================================================
echo  Checking PyInstaller and Python environment...
echo ==================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Python is not installed or not added to system PATH!
    pause
    exit /b
)

:: Install pyinstaller if not already present
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [i] PyInstaller not detected. Installing PyInstaller...
    python -m pip install pyinstaller
)

echo [✓] Python and PyInstaller detected.
echo [*] Compiling main.py into a single executable...

:: Build standalone EXE using PyInstaller
pyinstaller --onefile --clean --name="mobile_proto_generator" main.py

if %errorlevel% equ 0 (
    echo.
    echo ==================================================
    echo [✓] SUCCESS: Build completed successfully!
    echo Standalone executable is at: dist\mobile_proto_generator.exe
    echo ==================================================
) else (
    echo.
    echo [Error] PyInstaller compilation failed.
)

pause
