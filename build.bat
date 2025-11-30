@echo off
REM Build Attendux Sync Agent for Windows
REM Double-click this file to build

echo ======================================
echo Attendux Sync Agent Builder
echo ======================================
echo.

REM Check Python version
python --version
echo.

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
echo.

REM Build executable
echo Building executable...
pyinstaller --clean ^
    --onefile ^
    --windowed ^
    --name=Attendux-Sync-Agent ^
    --icon=logo.ico ^
    --hidden-import=PyQt5 ^
    --hidden-import=zk ^
    --hidden-import=requests ^
    attendux_sync_agent.py

echo.
echo ======================================
echo Build Complete!
echo ======================================
echo.
echo Executable location: dist\Attendux-Sync-Agent.exe
echo Size: ~20MB
echo.
echo Next steps:
echo 1. Test the executable: dist\Attendux-Sync-Agent.exe
echo 2. Create installer with Inno Setup (optional)
echo 3. Upload to: https://attendux.com/downloads/sync-agent
echo.

pause
