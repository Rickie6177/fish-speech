@echo off
echo ================================================================
echo   Fish Speech TTS API Launcher
echo ================================================================
echo.

:: Check if container is ALREADY running — skip restart if so
for /f "delims=" %%i in ('wsl -d Ubuntu -u root -- bash -c "docker ps --filter name=fish-speech-api --filter status=running --format {{.Names}} 2>/dev/null"') do set RUNNING=%%i
if "%RUNNING%"=="fish-speech-api" (
    echo [OK] Container is already running! No restart needed.
    echo      ^(To force restart, close this window and run start_api.bat again after:
    echo       wsl -d Ubuntu -u root -- docker stop fish-speech-api^)
    echo.
    goto :show_logs
)

echo [!] IMPORTANT: Close these apps to free GPU VRAM before starting:
echo     1. Wallpaper Engine (right-click tray icon, Quit)
echo     2. Steam
echo     3. NVIDIA GeForce Experience overlay
echo     4. Extra Edge/Chrome tabs
echo.
echo Press any key to start the API server...
pause >nul
echo.
echo Stopping old container (if any)...
wsl -d Ubuntu -u root -- bash -c "docker stop fish-speech-api 2>/dev/null; docker rm -f fish-speech-api 2>/dev/null"
echo.
echo Starting new container...
wsl -d Ubuntu -u root -- bash -c "docker run -d --gpus all --name fish-speech-api --restart unless-stopped -p 8080:8080 -e PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512 -e CUBLAS_WORKSPACE_CONFIG=:16:8 -v /mnt/e/fishtts/checkpoints:/app/checkpoints -v /mnt/e/fishtts/references:/app/references fish-speech-server:cuda"
echo.
echo Waiting for model to fully load (checking every 5s)...
:check_loop
timeout /t 5 /nobreak >nul
wsl -d Ubuntu -u root -- bash -c "docker logs fish-speech-api 2>&1 | grep -q 'Application startup complete'"
if %errorlevel% neq 0 (
    echo   Still loading...
    goto check_loop
)
echo.
echo ================================================================
echo   [SUCCESS] API is ready!
echo   Health: http://localhost:8080/v1/health
echo   TTS:    http://localhost:8080/v1/tts
echo ================================================================

:show_logs
echo.
echo [Following live logs below — press Ctrl+C to close this window]
echo ================================================================
wsl -d Ubuntu -u root -- bash -c "docker logs -f fish-speech-api 2>&1"
