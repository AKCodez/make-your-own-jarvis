@echo off
setlocal
cd /d "%~dp0"
title J.A.R.V.I.S.

rem ---- find Python 3.10 or newer
set "PY="
python -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)" >nul 2>nul && set "PY=python"
if not defined PY py -3 -c "import sys; sys.exit(0 if sys.version_info[:2] >= (3, 10) else 1)" >nul 2>nul && set "PY=py -3"
if not defined PY (
  echo.
  echo   Python 3.10 or newer isn't installed yet.
  echo   Get it free at https://www.python.org/downloads/
  echo   On the first installer screen, tick "Add python.exe to PATH", then run this again.
  echo.
  pause
  exit /b 1
)

rem ---- first run: private Python environment for JARVIS
if not exist ".venv\Scripts\python.exe" (
  echo.
  echo   First run: setting JARVIS up. This takes about 30 seconds...
  %PY% -m venv .venv
  if errorlevel 1 (
    echo   Couldn't create the Python environment. Try reinstalling Python.
    pause
    exit /b 1
  )
)

".venv\Scripts\python.exe" -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
  echo.
  echo   Installing failed. Check your internet connection and run this again.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" jarvis.py
echo.
pause
