@echo off
echo ========================================
echo  POLY-BOT STARTER
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo [2/3] Starting bot...
echo.

set DRY_RUN=false
python bot_late.py

echo.
echo [3/3] Bot stopped. Press any key to exit...
pause
