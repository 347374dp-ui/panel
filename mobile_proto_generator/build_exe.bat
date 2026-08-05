@echo off
title Bypass System EXE Builder
color 0a

echo ==================================================
echo         BYPASS SYSTEM STANDALONE BUILDER
echo ==================================================
echo  Starting compilation and packaging...
echo ==================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [Error] Python is not installed or not in your system PATH!
    echo Please install Python and try again.
    pause
    exit /b
)

:: 2. Build icon if logo.png is present
if exist logo.png (
    echo [*] Generating native icon file from logo.png...
    python icon_converter.py
)

:: 3. Install PyInstaller
echo [*] Checking/Installing PyInstaller...
python -m pip install --upgrade pip
python -m pip install pyinstaller
if %errorlevel% neq 0 (
    echo [Error] Failed to install PyInstaller via pip.
    pause
    exit /b
)
echo [✓] PyInstaller is ready.
echo.

:: 4. Compile Standalone Executable
echo [*] Compiling main.py into BypassLauncher.exe...
:: --onefile: single EXE
:: --name: BypassLauncher
:: --clean: clean cache
:: --icon: include native logo icon if it exists
if exist logo.ico (
    pyinstaller --onefile --clean --name=BypassLauncher --icon=logo.ico main.py
) else (
    pyinstaller --onefile --clean --name=BypassLauncher main.py
)

if %errorlevel% neq 0 (
    echo [Error] PyInstaller compilation failed!
    pause
    exit /b
)
echo [✓] Compilation successful! Standalone BypassLauncher.exe created in the 'dist' directory.
echo.

:: 5. Prepare Client Delivery Directory
echo [*] Preparing client delivery files...
if exist client_delivery_temp rmdir /s /q client_delivery_temp
mkdir client_delivery_temp

:: Copy compiled EXE, run_generator.bat, version file, and certificates
copy dist\BypassLauncher.exe client_delivery_temp\BypassLauncher.exe >nul
copy run_generator.bat client_delivery_temp\run_generator.bat >nul
if exist logo.png copy logo.png client_delivery_temp\logo.png >nul
if exist version.txt copy version.txt client_delivery_temp\version.txt >nul
if exist ca.crt copy ca.crt client_delivery_temp\ca.crt >nul
if exist ca.key copy ca.key client_delivery_temp\ca.key >nul

:: Create clean instructions file
echo ================================================== > client_delivery_temp\instructions.txt
echo              BYPASS CLIENT INSTRUCTIONS           >> client_delivery_temp\instructions.txt
echo ================================================== >> client_delivery_temp\instructions.txt
echo. >> client_delivery_temp\instructions.txt
echo To launch the system: >> client_delivery_temp\instructions.txt
echo 1. Simply double-click "BypassLauncher.exe" or run "run_generator.bat". >> client_delivery_temp\instructions.txt
echo 2. The launcher will automatically check and repair emulator caches, >> client_delivery_temp\instructions.txt
echo    verify and sync auto-updates, and generate randomized certificates >> client_delivery_temp\instructions.txt
echo    and fresh mobile device profiles for your emulator bypass proxy. >> client_delivery_temp\instructions.txt
echo. >> client_delivery_temp\instructions.txt
echo Troubleshooting "This app can't run on your PC" Error: >> client_delivery_temp\instructions.txt
echo - This occurs if the executable is truncated, corrupted during download, >> client_delivery_temp\instructions.txt
echo   or blocked by your web browser / antivirus smart-screen. >> client_delivery_temp\instructions.txt
echo - Try downloading the zip again or whitelist the file in Windows Defender. >> client_delivery_temp\instructions.txt
echo - Alternatively, you can run "run_generator.bat" or build from source >> client_delivery_temp\instructions.txt
echo   directly by running "build_exe.bat" locally on your machine! >> client_delivery_temp\instructions.txt
echo. >> client_delivery_temp\instructions.txt
echo Enjoy a secure, fully unique connection! >> client_delivery_temp\instructions.txt

:: 6. Create deliverable ZIP using Windows PowerShell (No external zip program required!)
echo [*] Packaging everything into client_delivery.zip for drive upload...
if exist client_delivery.zip del /f /q client_delivery.zip
powershell -Command "Compress-Archive -Path 'client_delivery_temp\*' -DestinationPath 'client_delivery.zip' -Force"
if %errorlevel% neq 0 (
    echo [Warning] PowerShell compression failed. You can zip the contents of 'client_delivery_temp' folder manually.
) else (
    echo [✓] Packaging Complete! client_delivery.zip is ready to upload to your Google Drive!
)

:: Clean up temporary build folders
rmdir /s /q client_delivery_temp
echo.
echo ==================================================
echo              BUILD PROCESS COMPLETE
echo ==================================================
echo.
pause
