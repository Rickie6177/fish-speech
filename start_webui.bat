@echo off
echo ================================================================
echo   Fish Speech TTS WebUI
echo ================================================================
echo.
echo Starting WebUI + API Proxy at http://localhost:8181
echo (API requests are proxied to WSL Docker automatically)
echo.
echo Press Ctrl+C to stop.
echo ================================================================
python "e:\fishtts\webui_server.py"
