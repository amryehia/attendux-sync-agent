# How to Generate the EXE File
# ============================================
# Step-by-step guide to create Attendux-Sync-Agent.exe
# ============================================

## 🚨 IMPORTANT: You Need Windows!

**Problem:** You're on macOS, but we need to build a Windows .exe file.

**Solutions:**

### Option 1: Use Windows PC/VM (Recommended)
### Option 2: Use Online Build Service
### Option 3: Use GitHub Actions (Automated)

---

## ✅ OPTION 1: Build on Windows PC/VM

### Step 1: Get Windows Environment
You need one of:
- Windows PC
- Windows VM (Parallels, VirtualBox, VMware)
- Boot Camp
- Ask someone with Windows

### Step 2: Install Python
```
1. Go to: https://www.python.org/downloads/
2. Download Python 3.11 (latest stable)
3. Run installer
4. ☑ Check "Add Python to PATH"
5. Click "Install Now"
```

### Step 3: Copy Project to Windows
Transfer the entire `sync-agent` folder to Windows:
```
- attendux_sync_agent.py
- requirements.txt
- build.bat
- icon.ico (if you have)
- logo.png (download from app.attendux.com)
```

### Step 4: Open Command Prompt as Administrator
```
Press Windows Key
Type: cmd
Right-click "Command Prompt"
Choose "Run as administrator"
```

### Step 5: Navigate to Project Folder
```cmd
cd C:\path\to\sync-agent
```

### Step 6: Install Dependencies
```cmd
pip install -r requirements.txt
pip install pyinstaller
```

### Step 7: Download Logo
```cmd
curl -o logo.png https://app.attendux.com/public/storage/logo.png
```

Or download manually and save as `logo.png`

### Step 8: Build EXE
```cmd
build.bat
```

Or manually:
```cmd
pyinstaller --onefile --windowed ^
    --name "Attendux-Sync-Agent" ^
    --icon=icon.ico ^
    --add-data "logo.png;." ^
    attendux_sync_agent.py
```

### Step 9: Get Your EXE!
```
Location: dist\Attendux-Sync-Agent.exe
Size: ~25-30 MB
```

### Step 10: Test It
```cmd
cd dist
Attendux-Sync-Agent.exe
```

Should open the app!

### Step 11: Upload to Server
```
Upload to: /Applications/XAMPP/xamppfiles/htdocs/payroll-attendance/applive/public/downloads/
URL: https://app.attendux.com/downloads/Attendux-Sync-Agent.exe
```

---

## 🌐 OPTION 2: Use Online Build Service

### Method A: GitHub Actions (FREE, Automated)

I'll create a GitHub Actions workflow that builds the .exe automatically!

**Steps:**
1. Create GitHub repo
2. Push code
3. GitHub builds .exe automatically
4. Download from Releases

See: `GITHUB_ACTIONS_BUILD.md`

### Method B: Replit (Quick Test)

1. Go to: https://replit.com
2. Create new Python project
3. Upload all files
4. Install dependencies
5. Run PyInstaller
6. Download .exe

**Note:** May have limitations

---

## 🤖 OPTION 3: GitHub Actions (BEST - Automated!)

I'll create this for you! It will:
- Build .exe automatically on every commit
- Create release with downloadable .exe
- Free and easy to use

See the workflow file I'll create next.

---

## 📦 What You'll Get

### File Info:
```
Name: Attendux-Sync-Agent.exe
Size: ~25-30 MB
Type: Windows Executable
Requires: Windows 10/11 (64-bit)
No Installation Required: Just double-click!
```

### Contents:
- Python runtime (embedded)
- PyQt5 GUI library
- pyzk ZKTeco library
- requests HTTP library
- Your application code
- Logo image
- All dependencies

---

## 🎯 Quick Summary

### If you have Windows access:
```bash
# On Windows:
cd sync-agent
pip install -r requirements.txt
pip install pyinstaller
curl -o logo.png https://app.attendux.com/public/storage/logo.png
build.bat

# Result:
# dist/Attendux-Sync-Agent.exe ✅
```

### If you DON'T have Windows:
```
Use GitHub Actions (I'll set it up for you!)
Just push code → GitHub builds .exe → Download
```

---

## 🔧 Troubleshooting Build Issues

### Error: "Python not found"
**Solution:**
```
Add Python to PATH:
1. Search "Environment Variables"
2. Edit "Path"
3. Add: C:\Python311\
4. Add: C:\Python311\Scripts\
5. Restart Command Prompt
```

### Error: "pip not found"
**Solution:**
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Error: "PyInstaller failed"
**Solution:**
```cmd
pip uninstall pyinstaller
pip install pyinstaller==5.13.0
```

### Error: "Missing module: PyQt5"
**Solution:**
```cmd
pip install PyQt5==5.15.9
```

### Error: "Missing logo.png"
**Solution:**
```cmd
curl -o logo.png https://app.attendux.com/public/storage/logo.png
```

Or download manually from browser

### Error: ".exe is too large (>100MB)"
**Solution:**
```cmd
# Use --onefile instead of --onedir
# Remove --debug flag
# This is normal, exe will be 25-30MB
```

### Error: ".exe won't run on Windows 10"
**Solution:**
```
Build on Windows 10, not Windows 11
Or use compatibility mode
```

---

## 📤 After Building

### Step 1: Test the EXE
```
1. Copy to clean Windows PC
2. Double-click Attendux-Sync-Agent.exe
3. Enter license: ATX-C83E-9317-46D1-91E6
4. Verify it connects and loads devices
5. Test sync
```

### Step 2: Upload to Server
```bash
# On Mac, upload via FTP/SCP:
scp dist/Attendux-Sync-Agent.exe \
    user@app.attendux.com:/path/to/public/downloads/

# Or use cPanel File Manager
# Or use FTP client (FileZilla)
```

### Step 3: Update Website
Add download link to landing page:
```html
<a href="https://app.attendux.com/downloads/Attendux-Sync-Agent.exe" 
   class="btn btn-primary">
    Download Sync Agent (Windows)
</a>
```

### Step 4: Send to Customer
```
Email template:

Subject: Attendux Sync Agent - Easy Setup

Hi [Customer],

Download the Attendux Sync Agent here:
https://app.attendux.com/downloads/Attendux-Sync-Agent.exe

Setup (2 minutes):
1. Download and run the file
2. Enter your license: ATX-C83E-9317-46D1-91E6
3. Click "Connect"
4. Click "Start Auto-Sync"
5. Done! It runs automatically in the background.

No router configuration needed!
No technical knowledge required!

Support: support@attendux.com

Best regards,
Attendux Team
```

---

## 🎉 That's It!

Once you build the .exe:
- ✅ Upload to: app.attendux.com/downloads/
- ✅ Send link to customers
- ✅ They download and run
- ✅ No installation, no setup, just works!

**Easiest solution for ZKTeco sync!**

---

## 🤝 Need Help?

### I can help you:
1. ✅ Set up GitHub Actions (automatic builds)
2. ✅ Create build scripts
3. ✅ Test the application
4. ✅ Create installer (optional)
5. ✅ Add auto-update feature

### You need to:
1. Get Windows access (VM or PC)
2. Or use GitHub Actions (I'll set up)
3. Build the .exe
4. Upload to server
5. Send to customers

**Let me know which option you want!**

---

Created: November 30, 2025
Status: Ready to Build
Platform: Windows 10/11 (64-bit)
Size: ~25-30 MB
Requirements: Python 3.8+ (only for building, not for running)

============================================
