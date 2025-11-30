# 🚀 Quick Start - Build Your EXE in 3 Steps!

## You're on macOS - Here's What to Do:

### ⚡ FASTEST: Use GitHub Actions (Recommended)

**No Windows needed! GitHub builds it for you automatically!**

```bash
# Step 1: Push to GitHub
cd /Applications/XAMPP/xamppfiles/htdocs/payroll-attendance/sync-agent
git init
git add .
git commit -m "Initial commit"

# Step 2: Create repo on github.com and push
# (Create new repo on GitHub website first)
git remote add origin https://github.com/YOUR_USERNAME/attendux-sync-agent.git
git push -u origin main

# Step 3: Wait 5 minutes, then download!
# Go to: github.com/YOUR_USERNAME/attendux-sync-agent/actions
# Download the Attendux-Sync-Agent-Windows artifact
```

**That's it! You now have Attendux-Sync-Agent.exe** ✅

---

### 🖥️ OR: Use a Windows PC/VM

If you have access to Windows:

```cmd
:: Step 1: Open Command Prompt
cd C:\path\to\sync-agent

:: Step 2: Install dependencies
pip install -r requirements.txt
pip install pyinstaller

:: Step 3: Build
build.bat

:: Step 4: Get your EXE!
:: Located at: dist\Attendux-Sync-Agent.exe
```

---

## 📤 After Building:

### Upload to your server:
```bash
# Upload via SCP
scp dist/Attendux-Sync-Agent.exe \
    user@app.attendux.com:/var/www/html/applive/public/downloads/

# Or use cPanel File Manager
# Upload to: public/downloads/
```

### Update download link:
```
URL: https://app.attendux.com/downloads/Attendux-Sync-Agent.exe
```

### Send to customer:
```
Hi [Customer],

Download Attendux Sync Agent:
https://app.attendux.com/downloads/Attendux-Sync-Agent.exe

Setup:
1. Download and run
2. Enter license: ATX-C83E-9317-46D1-91E6
3. Click "Connect"
4. Click "Start Auto-Sync"

Done! No router configuration needed!
```

---

## 📚 Full Documentation:

- **BUILD_GUIDE.md** - Complete build instructions
- **GITHUB_ACTIONS_BUILD.md** - GitHub Actions tutorial
- **README.md** - Full project documentation

---

## 🆘 Need Help?

The GitHub Actions method is **recommended** because:
- ✅ No Windows PC needed
- ✅ Free
- ✅ Automatic
- ✅ Professional
- ✅ Easy to update

Just push your code to GitHub and it builds automatically!

**See: GITHUB_ACTIONS_BUILD.md for step-by-step tutorial**

---

Created: November 30, 2025
Status: Ready to build!
Recommended: GitHub Actions (free, automatic)
