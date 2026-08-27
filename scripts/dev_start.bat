@echo off
cd /d "%~dp0.."
if not exist ".venv\Scripts\activate.bat" (
  echo Virtualenv not found. Create with: python -m venv .venv
  pause
  exit /b 1
)
call .venv\Scripts\activate
echo Starting uvicorn with reload (development)...
.venv\Scripts\python -m uvicorn app.core.main:app --reload --host 127.0.0.1 --port 8000
