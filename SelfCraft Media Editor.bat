@echo off
title SelfCraft Media Editor
cd /d "%~dp0"

set PAYLOAD_DIR=sme_files

:: Detect venv either in root or inside payload (when distributed)
if exist ".venv\Scripts\activate.bat" (
    goto :start_root
) else if exist "%PAYLOAD_DIR%\.venv\Scripts\activate.bat" (
    goto :start_payload
) else (
    goto :setup_decider
)

:setup_decider
if exist "%PAYLOAD_DIR%\scripts\setup.bat" (
    goto :setup_payload
) else (
    goto :setup_root
)

:setup_root
echo.
echo  ============================================
echo   SelfCraft Media Editor — First Time Setup
echo  ============================================
echo.
echo  Setting up for the first time (root)...
echo  Please do not close this window.
echo.
call scripts\setup.bat
goto :eof

:setup_payload
echo.
echo  ============================================
echo   SelfCraft Media Editor — First Time Setup
echo  ============================================
echo.
echo  Setting up for the first time (payload)...
echo  Please do not close this window.
echo.
call %PAYLOAD_DIR%\scripts\setup.bat
goto :eof

:start_root
echo.
echo  Starting SelfCraft Media Editor (root)...
echo  Do not close this window while using the app.
echo.
call scripts\start.bat
goto :eof

:start_payload
echo.
echo  Starting SelfCraft Media Editor (payload)...
echo  Do not close this window while using the app.
echo.
call %PAYLOAD_DIR%\scripts\start.bat
goto :eof