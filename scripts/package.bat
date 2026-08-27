@echo off
cd /d "%~dp0.."

echo Creating distributable zip (excludes .git and .venv)...

set STAGING=%TEMP%\sme_package_stage
set PAYLOAD_DIR=sme_files

if exist "%STAGING%" rd /s /q "%STAGING%"
mkdir "%STAGING%"

echo Copying project into staging folder...
rem Copy all items except .git, .venv and the top-level self-launcher
for /f "delims=" %%I in ('dir /b /a') do (
	if /I not "%%I"==".git" if /I not "%%I"==".venv" if /I not "%%I"=="SelfCraft Media Editor.bat" (
		xcopy "%%I" "%STAGING%\%PAYLOAD_DIR%\%%I" /E /I /Y >nul
	)
)

echo Creating zip with launcher at root and payload in %PAYLOAD_DIR%...
powershell -NoProfile -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; `n[IO.Compression.ZipFile]::CreateFromDirectory('%STAGING%', Join-Path('%CD%','SelfCraft-Media-Editor.zip'))"

rem Now open the zip, replace top-level entries: we want the launcher at root.
rem Remove the current launcher entry if any and add the real one from cwd
powershell -NoProfile -Command "`n$zip='SelfCraft-Media-Editor.zip'; `n$temp='sme_temp.zip'; `nif(Test-Path $temp){Remove-Item $temp}; `nAdd-Type -AssemblyName System.IO.Compression.FileSystem; `n[IO.Compression.ZipFile]::ExtractToDirectory($zip, 'sme_extracted'); `nMove-Item -Path 'SelfCraft Media Editor.bat' -Destination 'sme_extracted' -Force; `nif(Test-Path $zip){Remove-Item $zip}; `n[IO.Compression.ZipFile]::CreateFromDirectory('sme_extracted', $zip); `nRemove-Item -Recurse -Force 'sme_extracted'"

echo Created: %CD%\SelfCraft-Media-Editor.zip
echo Cleaning up staging...
rd /s /q "%STAGING%"
echo Done.
pause
