#!/bin/bash
# ==============================================================================
# Cross-compilation script to build 64-bit Windows Executables under Linux (Wine)
# ==============================================================================
set -e

echo "[*] Setting up Wine environment..."
export WINEARCH=win64
export WINEPREFIX="$HOME/.wine64"

# Check if wine is installed
if ! command -v wine &> /dev/null; then
    echo "[!] wine is not installed. Installing wine and dependencies..."
    sudo dpkg --add-architecture i386
    sudo apt-get update
    sudo apt-get install -y wine wine64 wine32 cabextract wget
fi

# Download Python 3.10 for Windows (64-bit)
PYTHON_VER="3.10.11"
PYTHON_EXE="python-${PYTHON_VER}-amd64.exe"
if [ ! -f "$PYTHON_EXE" ]; then
    echo "[*] Downloading Python $PYTHON_VER for Windows (64-bit)..."
    wget -q "https://www.python.org/ftp/python/${PYTHON_VER}/${PYTHON_EXE}"
fi

# Install Python inside Wine
echo "[*] Installing Python inside Wine (silently)..."
wine "$PYTHON_EXE" /quiet InstallAllUsers=1 PrependPath=1

# Locate python.exe inside Wine prefix
# Standard path for Python in Wine is typically inside "C:\Program Files\Python310" or similar
echo "[*] Verifying python installation in Wine..."
sleep 5

# Check standard installation path or use wine python directly
echo "[*] Upgrading pip inside Wine..."
wine python -m pip install --upgrade pip || wine "C:\Program Files\Python310\python.exe" -m pip install --upgrade pip || true

echo "[*] Installing PyInstaller inside Wine..."
wine pip install pyinstaller || wine "C:\Program Files\Python310\python.exe" -m pip install pyinstaller || true

echo "[*] Running PyInstaller to cross-compile Windows Executable..."
wine pyinstaller --onefile --clean --name="mobile_proto_generator" main.py || wine "C:\Program Files\Python310\Scripts\pyinstaller.exe" --onefile --clean --name="mobile_proto_generator" main.py

echo "[✓] Build complete! Standalone Windows executable is located in 'dist/mobile_proto_generator.exe'"
