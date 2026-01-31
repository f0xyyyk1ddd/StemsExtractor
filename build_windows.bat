@echo off
TITLE Building StemsExtractor for Windows
CLS

ECHO ===================================================
ECHO      StemsExtractor for Windows - Build Script
ECHO ===================================================
ECHO.
ECHO This script will set up a virtual environment and build the .exe
ECHO.

:: Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERROR] Python is not installed or not in PATH.
    ECHO Please install Python 3.9 from python.org and try again.
    PAUSE
    EXIT /B
)

:: Create VENV
ECHO [1/4] Creating virtual environment...
if exist venv rmdir /s /q venv
python -m venv venv

:: Install Requirements
ECHO [2/4] Installing dependencies...
call venv\Scripts\activate
pip install --upgrade pip
pip install PyQt5 spleeter static-ffmpeg pyinstaller

:: Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Build
ECHO [3/4] Building application...
pyinstaller GuiApp.spec

ECHO.
ECHO [4/4] Build Complete!
ECHO You can find the executable in the 'dist' folder.
ECHO.
PAUSE
