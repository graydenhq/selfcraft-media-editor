@echo off
cd /d "%~dp0.."
call .venv\Scripts\activate

:: Start server in a new window using the venv Python
echo  Starting server in a new window...
start "SME Server" cmd /c ".venv\Scripts\python -m uvicorn app.core.main:app --host 127.0.0.1 --port 8000"

:: Wait for server to be ready (poll /health) with simple progress dots
echo  Waiting for server to start...
powershell -NoProfile -Command "for ($i=0; $i -lt 60; $i++) { try { $r=(New-Object Net.WebClient).DownloadString('http://127.0.0.1:8000/health'); if ($r) { Write-Host ''; exit 0 } } catch { Write-Host -NoNewline '.'; Start-Sleep -Seconds 1 } } Write-Host ''; exit 1"

:: Open dashboard in default browser (served over HTTP)
start "" "http://127.0.0.1:8000/"

echo.
echo  SelfCraft Media Editor launched. The server runs in a separate window.
echo  Close the "SME Server" window to stop the server.
echo.
pause