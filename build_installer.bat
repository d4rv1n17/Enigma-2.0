@echo off
setlocal
cd /d "%~dp0"
title Enigma Cube - building the installer
echo.
echo ==========================================
echo   Enigma Cube - building Setup.exe
echo ==========================================
echo.

echo Looking for Python...
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY goto :nopython
%PY% --version || goto :nopython

echo.
echo Installing build tools: PyQt5, PyInstaller...
%PY% -m pip install --upgrade -r requirements.txt pyinstaller || goto :fail

echo.
%PY% installer\build.py || goto :fail

echo.
echo ==========================================
echo   DONE! The installer is in the Output folder.
echo ==========================================
explorer "%~dp0Output"
pause
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
