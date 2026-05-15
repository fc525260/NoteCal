@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"
set "SCRIPT_DIR=%cd%"

if exist "%SCRIPT_DIR%\.venv\Scripts\python.exe" (
    "%SCRIPT_DIR%\.venv\Scripts\python.exe" "%SCRIPT_DIR%\run.py"
) else (
    python -m venv "%SCRIPT_DIR%\.venv"
    "%SCRIPT_DIR%\.venv\Scripts\pip.exe" install -r "%SCRIPT_DIR%\requirements.txt"
    "%SCRIPT_DIR%\.venv\Scripts\python.exe" "%SCRIPT_DIR%\run.py"
)

endlocal