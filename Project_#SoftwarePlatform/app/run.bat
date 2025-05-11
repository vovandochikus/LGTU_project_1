@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

if not exist "%SCRIPT_DIR%venv" (
	python -m venv "%SCRIPT_DIR%venv"
)
start cmd /k "call cd /d %userprofile%/desktop/Project_#SoftwarePlatform/app && python app.py"
start cmd /k "call %SCRIPT_DIR%venv\Scripts\activate && pip install -r %SCRIPT_DIR%requirements.txt && set PYTHONPATH=. && set PYTHONHOME=%SCRIPT_DIR%venv"
start "" "http://127.0.0.1:5000"
