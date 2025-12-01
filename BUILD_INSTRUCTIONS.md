# Build Desktop App - Build #24

## Quick Build Command (Windows)

```bash
cd sync-agent
pyinstaller attendux_sync_agent.spec --clean
```

## Or Full Build from Scratch:

```bash
cd sync-agent
pyinstaller --clean --onefile --windowed \
    --name "Attendux Sync Agent" \
    --icon=app_icon.ico \
    --add-data "app_icon.ico;." \
    attendux_sync_agent.py
```

## After Build:

1. Executable will be in: `sync-agent/dist/Attendux Sync Agent.exe`
2. Test on Windows 11
3. Check for flash/flicker - should be gone!

## Build #24 Changes:
- Disabled WebGL rendering
- Disabled Accelerated 2D Canvas
- Enabled opaque paint events
- Prevents flash/flicker during page loads

## Test Checklist:
- [ ] Login works
- [ ] Dashboard loads without flash
- [ ] Navigate to Employees - no flash
- [ ] Navigate to Reports - no flash
- [ ] Navigate to Devices - no flash
- [ ] Overall smooth experience
