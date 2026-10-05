@echo off
REM Run app.exe in background with logs in the same folder

set APP_PATH=%~dp0app.exe
set LOG_FILE=%~dp0logs.txt

echo [*] Starting app.exe in background...
start "" "%APP_PATH%" > "%LOG_FILE%" 2>&1

echo [✔] app.exe started successfully in background.
echo Logs will be written to "%LOG_FILE%".
pause
