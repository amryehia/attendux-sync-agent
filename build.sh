#!/bin/bash
# Build Attendux Sync Agent for Windows
# Run this on Windows with Python 3.8+ installed

echo "======================================"
echo "Attendux Sync Agent Builder"
echo "======================================"
echo ""

# Check Python version
python --version

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Build executable
echo ""
echo "Building executable..."
pyinstaller --clean \
    --onefile \
    --windowed \
    --name="Attendux-Sync-Agent" \
    --icon=logo.ico \
    --add-data="logo.png;." \
    --hidden-import=PyQt5 \
    --hidden-import=zk \
    --hidden-import=requests \
    attendux_sync_agent.py

echo ""
echo "======================================"
echo "Build Complete!"
echo "======================================"
echo ""
echo "Executable location: dist/Attendux-Sync-Agent.exe"
echo "Size: ~20MB"
echo ""
echo "Next steps:"
echo "1. Test the executable: dist/Attendux-Sync-Agent.exe"
echo "2. Create installer with Inno Setup (optional)"
echo "3. Upload to: https://attendux.com/downloads/sync-agent"
echo ""
