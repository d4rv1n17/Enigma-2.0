@echo off
setlocal
cd /d "%~dp0"
title Enigma Cube - building the installer
echo.
echo ==========================================
echo   Enigma Cube - building Setup.exe
echo ==========================================
echo.

echo [1/4] Looking for Python...
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY goto :nopython
%PY% --version || goto :nopython

echo.
echo [2/4] Installing build tools: PyQt5, PyInstaller, Pillow...
%PY% -m pip install --upgrade -r requirements.txt pyinstaller pillow || goto :fail

echo.
echo [3/4] Building EnigmaCube.exe...
if exist build rmdir /s /q build
if exist dist\EnigmaCube rmdir /s /q dist\EnigmaCube
%PY% -m PyInstaller --noconfirm --clean --onedir --windowed --name EnigmaCube --icon assets\app.ico --add-data "assets;assets" --version-file installer\version_info.txt main.py || goto :fail
if not exist dist\EnigmaCube\EnigmaCube.exe goto :fail

echo.
echo [4/4] Building the installer with Inno Setup...
call :findiscc
if defined ISCC goto :haveiscc
echo Inno Setup is not installed - trying to install it with winget...
winget install --id JRSoftware.InnoSetup -e --accept-package-agreements --accept-source-agreements
call :findiscc
if defined ISCC goto :haveiscc
echo.
echo Could not find Inno Setup 6.
echo Download and install it from https://jrsoftware.org/isdl.php
echo then run this file again.
goto :fail

:haveiscc
"%ISCC%" installer\EnigmaCube.iss || goto :fail

echo.
echo ==========================================
echo   DONE!  Installer:
echo   %~dp0Output\EnigmaCube-Setup-2.2.exe
echo ==========================================
explorer "%~dp0Output"
pause
exit /b 0

:findiscc
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
exit /b 0

:nopython
echo.
echo Python 3.8+ was not found.
echo Install it from https://www.python.org/downloads/
echo and tick "Add python.exe to PATH" in the installer, then run this file again.
goto :fail

:fail
echo.
echo ******** BUILD FAILED - scroll up to see the error ********
pause
exit /b 1
