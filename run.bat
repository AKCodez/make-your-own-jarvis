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

%PY% jarvis.py
echo.
pause
