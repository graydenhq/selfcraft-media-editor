@echo off
cd /d "%~dp0.."

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Python is not installed.
    echo  Opening the Python download page now.
    echo.
    echo  When it opens:
    echo  1. Click the big Download button
    echo  2. Run the installer
    echo  3. TICK "Add python.exe to PATH" on the first screen
    echo  4. Click Install Now
    echo  5. Come back here and press any key when done.
    echo.
    start https://python.org/downloads
    pause
)

:: Check FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Installing FFmpeg...
    winget install ffmpeg
    echo.
    echo  FFmpeg installed.
    echo  Please close this window, reopen it, and run
    echo  "SelfCraft Media Editor.bat" again.
    echo.
    pause
    exit
)

:: Create virtual environment
echo  Setting up the application environment...
if not exist .venv (
    python -m venv .venv
)

:: Install libraries
echo  Installing required libraries (this may take a few minutes)...
call .venv\Scripts\activate
pip install fastapi uvicorn openai-whisper watchdog python-multipart --quiet

:: Ask which Whisper model to download (optional)
echo.
echo Which Whisper model would you like to download for transcription?
echo  [T]iny (~75MB)   [B]ase (~140MB)   [S]mall (~460MB)   [N]one (skip now)
set /p MODEL_CHOICE=Enter T/B/S/N (default B):
if "%MODEL_CHOICE%"=="" set MODEL_CHOICE=B
set MODEL=none
if /I "%MODEL_CHOICE%"=="T" set MODEL=tiny
if /I "%MODEL_CHOICE%"=="B" set MODEL=base
if /I "%MODEL_CHOICE%"=="S" set MODEL=small
if /I "%MODEL_CHOICE%"=="N" set MODEL=none

if /I "%MODEL%"=="none" (
    echo Skipping Whisper model download. You can download later from the Settings.
) else (
    echo Downloading Whisper model "%MODEL%" (this may take some minutes)...
    .venv\Scripts\python scripts\download_model.py %MODEL%
    if errorlevel 1 (
        echo Model download failed or was cancelled.
        echo Please re-run setup.bat to try again, or download a smaller model.
        pause
        exit /b 1
    )
)

:: Create media folders on Desktop
echo  Creating your media folders on the Desktop...
set MEDIA=%USERPROFILE%\Desktop\SelfCraft Media
if not exist "%MEDIA%\Raw Videos\Recorded Classes" mkdir "%MEDIA%\Raw Videos\Recorded Classes"
if not exist "%MEDIA%\Raw Videos\Teaching Reels" mkdir "%MEDIA%\Raw Videos\Teaching Reels"
if not exist "%MEDIA%\Raw Videos\Testimonials" mkdir "%MEDIA%\Raw Videos\Testimonials"
if not exist "%MEDIA%\Edited Videos" mkdir "%MEDIA%\Edited Videos"
if not exist "%MEDIA%\Temp" mkdir "%MEDIA%\Temp"
if not exist "%MEDIA%\Review" mkdir "%MEDIA%\Review"

:: Write config with correct Windows paths
echo  Configuring folder paths...
python -c "
import json, os
config_path = 'config/settings.json'
with open(config_path) as f:
    cfg = json.load(f)
base = os.path.join(os.path.expanduser('~'), 'Desktop', 'SelfCraft Media')
cfg['folders']['raw_videos'] = base.replace('\\\\', '/') + '/Raw Videos'
cfg['folders']['edited_videos'] = base.replace('\\\\', '/') + '/Edited Videos'
cfg['folders']['temp'] = base.replace('\\\\', '/') + '/Temp'
cfg['review_folder'] = base.replace('\\\\', '/') + '/Review'
cfg['file_manager'] = 'explorer'
with open(config_path, 'w') as f:
    json.dump(cfg, f, indent=2)
print('Config updated.')
"

echo.
echo  ============================================
echo   Setup complete!
echo  ============================================
echo.
echo  Your media folders are on your Desktop
echo  inside a folder called "SelfCraft Media".
echo.
echo  Double-click "SelfCraft Media Editor.bat"
echo  to launch the app.
echo.
pause