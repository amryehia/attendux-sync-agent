# 🛠️ How to Build the EXE File for Customers
# ============================================
# Follow these steps to create Attendux-Sync-Agent.exe
# ============================================

## 📋 Prerequisites (One-Time Setup)

### Step 1: Install Python
1. Download Python from: https://www.python.org/downloads/
2. Choose: **Python 3.11.x** or **Python 3.10.x** (recommended)
3. ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click "Install Now"

### Step 2: Verify Installation
Open Command Prompt (Windows Key + R, type `cmd`, press Enter):
```cmd
python --version
```
Should show: `Python 3.11.x` or similar

---

## 🚀 Building the EXE (Every Time You Update)

### Quick Method (Recommended):

1. **Open File Explorer**
   - Navigate to: `payroll-attendance/sync-agent/`

2. **Download Logo** (First time only)
   - Open browser: https://app.attendux.com/public/storage/logo.png
   - Right-click → Save As → `logo.png`
   - Save it in the `sync-agent/` folder

3. **Convert Logo to ICO** (First time only)
   - Go to: https://convertio.co/png-ico/
   - Upload `logo.png`
   - Download `logo.ico`
   - Save it in the `sync-agent/` folder

4. **Double-Click `build.bat`**
   - Wait 2-3 minutes
   - You'll see a window with progress

5. **Done!**
   - The EXE file will be in: `sync-agent/dist/Attendux-Sync-Agent.exe`

---

## 📦 What You'll Get

After building, you'll have:

```
sync-agent/
├── dist/
│   └── Attendux-Sync-Agent.exe  ← This is what you send to customers!
│                                   (~20-25 MB)
├── build/                       ← Temporary files (can delete)
└── Attendux-Sync-Agent.spec    ← Build config (auto-generated)
```

---

## 🎯 Manual Method (If Double-Click Doesn't Work)

### Step 1: Open Command Prompt
```cmd
cd C:\Applications\XAMPP\xamppfiles\htdocs\payroll-attendance\sync-agent
```

### Step 2: Install Requirements
```cmd
pip install -r requirements.txt
```

### Step 3: Build
```cmd
build.bat
```

Or run directly:
```cmd
pyinstaller --clean --onefile --windowed --name=Attendux-Sync-Agent --icon=logo.ico attendux_sync_agent.py
```

---

## 📤 Sending to Customer

### Option 1: Direct Download (Recommended)

1. **Upload to Your Server**
   ```
   Upload: dist/Attendux-Sync-Agent.exe
   To: https://app.attendux.com/public/downloads/
   ```

2. **Send Link to Customer**
   ```
   Download: https://app.attendux.com/public/downloads/Attendux-Sync-Agent.exe
   ```

### Option 2: Email Attachment

⚠️ **Problem:** 20 MB file might be too large for email

**Solution:** Use file sharing:
- Google Drive
- Dropbox
- WeTransfer
- OneDrive

### Option 3: WhatsApp/Telegram

- Compress first: Right-click → Send to → Compressed folder
- Send the `.zip` file

---

## ✅ Testing Before Sending

### Test on Your Windows PC:

1. **Copy EXE to Desktop**
   ```
   Copy: sync-agent/dist/Attendux-Sync-Agent.exe
   To: Desktop
   ```

2. **Double-Click to Run**

3. **Enter Test License**
   ```
   License: ATX-C83E-9317-46D1-91E6
   ```

4. **Click "Connect"**
   - Should show: ✅ Connected - Movera
   - Should load: 1 device (ZKTeco Main)

5. **Click "Sync Now"**
   - Should show: ✅ Sync completed!

6. **If All Tests Pass:**
   - ✅ EXE is ready to send!

---

## 🔧 Troubleshooting Build Issues

### Problem 1: "Python not found"
**Solution:**
```cmd
# Add Python to PATH manually
# Windows Key → Search "Environment Variables"
# Edit System PATH → Add: C:\Users\YourName\AppData\Local\Programs\Python\Python311
```

### Problem 2: "pip not found"
**Solution:**
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Problem 3: "PyInstaller not found"
**Solution:**
```cmd
pip install pyinstaller
```

### Problem 4: Build fails with errors
**Solution:**
```cmd
# Clean and retry
rmdir /s /q build dist
del Attendux-Sync-Agent.spec
build.bat
```

### Problem 5: EXE won't run (Windows Defender blocks it)
**Solution:**
```
This is normal for unsigned executables.

Customer needs to:
1. Click "More info"
2. Click "Run anyway"

Or you can sign the EXE (costs money):
- Buy code signing certificate ($100-300/year)
- Use SignTool.exe to sign the EXE
```

---

## 📁 Where to Upload for Customers

### Your Server (app.attendux.com):

1. **Via cPanel File Manager:**
   ```
   1. Login to cPanel
   2. File Manager → public_html/applive/public/
   3. Create folder: "downloads"
   4. Upload: Attendux-Sync-Agent.exe
   5. Set permissions: 755 (read/execute)
   ```

2. **Via FTP:**
   ```
   Host: app.attendux.com
   Username: Your cPanel username
   Password: Your cPanel password
   Upload to: /public_html/applive/public/downloads/
   ```

3. **Download URL:**
   ```
   https://app.attendux.com/public/downloads/Attendux-Sync-Agent.exe
   ```

---

## 📝 Customer Installation Instructions

### Simple Version (Send this to customer):

```
تحميل وتثبيت برنامج المزامنة
Download and Install Sync Agent

1. حمّل البرنامج / Download:
   https://app.attendux.com/public/downloads/Attendux-Sync-Agent.exe

2. شغّل الملف / Run the file:
   دبل كليك على الملف
   Double-click the file

3. إذا ظهر تحذير Windows:
   If Windows warning appears:
   اضغط "More info" → "Run anyway"
   Click "More info" → "Run anyway"

4. حط رقم الترخيص:
   Enter license:
   ATX-C83E-9317-46D1-91E6

5. اضغط "Connect"
   Click "Connect"

6. اضغط "Start Auto-Sync"
   Click "Start Auto-Sync"

7. تم! البرنامج يشتغل تلقائياً
   Done! Program runs automatically
```

---

## 🔄 Updating the App

### When you make changes to the code:

1. **Edit Python file:**
   ```
   sync-agent/attendux_sync_agent.py
   ```

2. **Rebuild EXE:**
   ```
   Double-click: build.bat
   ```

3. **Test new version**

4. **Upload new EXE:**
   ```
   Replace old file at:
   https://app.attendux.com/public/downloads/Attendux-Sync-Agent.exe
   ```

5. **Notify customers:**
   ```
   "New version available! Download and replace old file."
   ```

---

## 📊 Build Checklist

Before sending to customer:

- [ ] Logo downloaded and converted to .ico
- [ ] All URLs updated to app.attendux.com
- [ ] Python app tested locally
- [ ] build.bat executed successfully
- [ ] EXE created in dist/ folder
- [ ] EXE tested on clean Windows PC
- [ ] License verification works
- [ ] Device loading works
- [ ] Sync works
- [ ] System tray icon works
- [ ] EXE uploaded to server
- [ ] Download link tested
- [ ] Customer instructions prepared

---

## 💾 File Sizes

**Typical sizes:**
```
Attendux-Sync-Agent.exe:  ~20-25 MB
Compressed (.zip):        ~8-10 MB
```

**Why so big?**
- Includes entire Python runtime
- Includes PyQt5 GUI libraries
- Includes all dependencies
- But: Customer only downloads once!

---

## 🎯 Quick Reference

### Build Command:
```cmd
cd sync-agent
build.bat
```

### Output Location:
```
sync-agent/dist/Attendux-Sync-Agent.exe
```

### Upload To:
```
https://app.attendux.com/public/downloads/Attendux-Sync-Agent.exe
```

### Customer Downloads From:
```
https://app.attendux.com/public/downloads/Attendux-Sync-Agent.exe
```

---

## 🆘 Need Help?

### If build fails:
1. Check Python installed correctly
2. Check all files present (attendux_sync_agent.py, requirements.txt, logo.ico)
3. Try cleaning: `rmdir /s /q build dist`
4. Run build.bat again

### If EXE doesn't work:
1. Test on different Windows PC
2. Check Windows Defender didn't block it
3. Run as Administrator
4. Check error logs in: `%USERPROFILE%\.attendux_sync\`

---

**Created:** November 30, 2025  
**For:** Attendux Sync Agent v1.0  
**Platform:** Windows 10/11  
**Build Tool:** PyInstaller  

✅ **Follow this guide to create the EXE file for your customers!**

============================================
