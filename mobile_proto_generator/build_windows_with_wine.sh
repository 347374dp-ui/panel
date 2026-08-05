#!/bin/bash
# ==============================================================================
# Cross-compilation script to build 64-bit Windows Executables under Linux (Wine)
# Using fail-safe Windows Embeddable Python distribution to bypass headless MSI/installer limits.
# ==============================================================================
set -e

echo "[*] Setting up Wine environment..."
export WINEARCH=win64
export WINEPREFIX="$HOME/.wine64"

# Ensure Wine configuration folder exists and is initialized
mkdir -p "$WINEPREFIX"

# Check if wine is installed
if ! command -v wine &> /dev/null; then
    echo "[!] wine is not installed. Installing wine and dependencies..."
    sudo dpkg --add-architecture i386
    sudo apt-get update
    sudo apt-get install -y wine wine64 wine32 cabextract wget unzip
fi

# Download Portable Python embeddable package (64-bit Windows)
PYTHON_ZIP="python-3.10.11-embed-amd64.zip"
if [ ! -f "$PYTHON_ZIP" ]; then
    echo "[*] Downloading Portable Python 3.10.11 zip for Windows..."
    wget -q "https://www.python.org/ftp/python/3.10.11/$PYTHON_ZIP"
fi

# Extract embeddable Python directly into Wine C: drive to bypass any installer error 183
PYTHON_DIR="$WINEPREFIX/drive_c/python"
echo "[*] Extracting portable Python to Wine C: drive ($PYTHON_DIR)..."
mkdir -p "$PYTHON_DIR"
unzip -o -q "$PYTHON_ZIP" -d "$PYTHON_DIR"

# Enable site-packages (pip and third-party libs) in embeddable distribution
echo "[*] Enabling site-packages in embeddable Python config..."
sed -i 's/#import site/import site/g' "$PYTHON_DIR/python310._pth"

# Download pip bootstrap utility
if [ ! -f "get-pip.py" ]; then
    echo "[*] Downloading pip bootstrap installer..."
    wget -q "https://bootstrap.pypa.io/get-pip.py"
fi

# Install pip inside Wine's portable Python environment
echo "[*] Installing pip inside Wine portable Python..."
wine "$PYTHON_DIR/python.exe" get-pip.py --quiet

# Install PyInstaller inside portable Python
echo "[*] Installing PyInstaller inside Wine portable Python..."
wine "$PYTHON_DIR/python.exe" -m pip install --quiet pyinstaller

# Run PyInstaller to cross-compile Windows Executable
echo "[*] Running PyInstaller to cross-compile standalone Windows Executable..."
wine "$PYTHON_DIR/Scripts/pyinstaller.exe" --onefile --clean --name="mobile_proto_generator" main.py

echo "[✓] Build complete! Standalone Windows executable is located in 'dist/mobile_proto_generator.exe'"
