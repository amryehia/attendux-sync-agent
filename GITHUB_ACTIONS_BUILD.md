# GitHub Actions - Automatic EXE Builder
# ============================================
# This will build your .exe automatically on GitHub!
# No Windows PC needed!
# ============================================

## 🎯 What This Does

Every time you push code to GitHub:
1. GitHub automatically builds the Windows .exe
2. Creates a release with downloadable file
3. You download and upload to your server

**FREE and AUTOMATIC!**

---

## 📋 Setup Steps

### Step 1: Create GitHub Repository

```bash
# On your Mac:
cd /Applications/XAMPP/xamppfiles/htdocs/payroll-attendance/sync-agent

# Initialize git
git init

# Add files
git add .
git commit -m "Initial commit - Attendux Sync Agent"

# Create repo on GitHub.com:
# 1. Go to github.com
# 2. Click "New Repository"
# 3. Name: attendux-sync-agent
# 4. Click "Create"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/attendux-sync-agent.git
git branch -M main
git push -u origin main
```

### Step 2: Add GitHub Actions Workflow

I'll create the workflow file for you (see below).

### Step 3: Wait for Build

```
1. Push code to GitHub
2. Go to "Actions" tab
3. Watch it build (takes ~5 minutes)
4. Download .exe from "Releases"
```

---

## 📄 Workflow File

Create this file: `.github/workflows/build-exe.yml`

```yaml
name: Build Windows EXE

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Download logo
      run: |
        curl -o logo.png https://app.attendux.com/public/storage/logo.png
    
    - name: Build EXE
      run: |
        pyinstaller --onefile --windowed `
          --name "Attendux-Sync-Agent" `
          --add-data "logo.png;." `
          attendux_sync_agent.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: Attendux-Sync-Agent
        path: dist/Attendux-Sync-Agent.exe
    
    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: dist/Attendux-Sync-Agent.exe
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🚀 How to Use

### First Time Setup:

1. **Create folder structure:**
   ```bash
   cd sync-agent
   mkdir -p .github/workflows
   ```

2. **Copy the workflow file above to:**
   ```
   .github/workflows/build-exe.yml
   ```

3. **Push to GitHub:**
   ```bash
   git add .github/workflows/build-exe.yml
   git commit -m "Add automatic build workflow"
   git push
   ```

4. **Watch it build:**
   - Go to your repo on GitHub
   - Click "Actions" tab
   - See the build running
   - Wait ~5 minutes

5. **Download the .exe:**
   - Click on the completed workflow
   - Scroll down to "Artifacts"
   - Download "Attendux-Sync-Agent"
   - Extract the .exe file

### For Future Updates:

1. **Make changes to code**
2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Update: improved sync logic"
   git push
   ```
3. **GitHub rebuilds automatically!**
4. **Download new .exe from Artifacts**

### Create Release Version:

```bash
# Tag a release version
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release"
git push origin v1.0.0

# GitHub will:
# 1. Build the .exe
# 2. Create a Release
# 3. Attach .exe to Release
# 4. Customers can download from Releases page!
```

---

## 📦 Alternative: Manual Build Workflow

If you can't use GitHub Actions, use this manual workflow:

### Option A: Ask a Friend with Windows

1. Send them the `sync-agent` folder
2. They run `build.bat`
3. They send you back `dist/Attendux-Sync-Agent.exe`
4. Done!

### Option B: Rent Windows VPS

1. DigitalOcean Windows Droplet ($12/month)
2. AWS EC2 Windows (free tier available)
3. Azure Windows VM (free tier available)
4. Use for 1 hour to build, then delete

**Steps:**
```powershell
# On Windows VPS:
# 1. Install Python
# 2. Clone repo
# 3. Build
cd sync-agent
pip install -r requirements.txt
pip install pyinstaller
build.bat

# 4. Download the exe
# 5. Delete VPS
```

### Option C: Docker + Wine (Advanced)

You can try building on Mac using Wine, but it's complicated and may not work perfectly.

---

## ✅ Recommended Approach

**Best Option: GitHub Actions**

Why?
- ✅ FREE
- ✅ Automatic
- ✅ No Windows PC needed
- ✅ Professional
- ✅ Customers can download from Releases
- ✅ Version tracking
- ✅ Build logs
- ✅ Easy updates

**Just 3 commands:**
```bash
cd sync-agent
mkdir -p .github/workflows
# Copy workflow file
git add .
git commit -m "Add auto-build"
git push
```

**Done! 🎉**

---

## 🎓 Tutorial: Complete GitHub Setup

### 1. Create GitHub Account
- Go to github.com
- Sign up (free)

### 2. Install Git on Mac
```bash
# Check if installed
git --version

# If not installed:
brew install git
```

### 3. Create Repository
```bash
cd /Applications/XAMPP/xamppfiles/htdocs/payroll-attendance/sync-agent

git init
git add .
git commit -m "Initial commit"
```

### 4. Create Repo on GitHub
- Go to github.com
- Click green "New" button
- Repository name: `attendux-sync-agent`
- Click "Create repository"

### 5. Push Code
```bash
# Copy the commands from GitHub (they look like this):
git remote add origin https://github.com/YOUR_USERNAME/attendux-sync-agent.git
git branch -M main
git push -u origin main
```

### 6. Add Workflow
```bash
mkdir -p .github/workflows
nano .github/workflows/build-exe.yml
# Paste the workflow YAML from above
# Press Ctrl+O to save, Ctrl+X to exit

git add .github
git commit -m "Add build workflow"
git push
```

### 7. Watch Build
- Go to your repo on GitHub
- Click "Actions" tab
- See it building!
- After 5 minutes, click on the workflow
- Download artifact

### 8. Upload to Your Server
```bash
# Download from GitHub to Mac
# Then upload to server:
scp Attendux-Sync-Agent.exe user@app.attendux.com:/var/www/html/applive/public/downloads/
```

**Done! 🎉**

---

## 💡 Pro Tips

### Tip 1: Automatic Releases
Every time you create a tag, GitHub creates a downloadable release:
```bash
git tag v1.0.0
git push origin v1.0.0

# Creates release at:
# https://github.com/YOUR_USERNAME/attendux-sync-agent/releases
```

### Tip 2: Add Icon
```yaml
# In build-exe.yml, add:
--icon=icon.ico
```

First create/download an icon:
```bash
# Convert PNG to ICO using online tool:
# https://convertio.co/png-ico/
```

### Tip 3: Version Info
Add version to exe:
```python
# In attendux_sync_agent.py, add:
VERSION = "1.0.0"
```

### Tip 4: Code Signing (Optional)
For production, sign the .exe to avoid Windows SmartScreen warnings.

---

## 🆘 Troubleshooting

### Build Fails: "Python not found"
**Fix:** Workflow already includes Python setup, should work

### Build Fails: "Cannot download logo"
**Fix:** Make sure logo is accessible at:
```
https://app.attendux.com/public/storage/logo.png
```

### Build Fails: "Module not found"
**Fix:** Add missing module to requirements.txt

### Can't Download Artifact
**Fix:** 
1. Make sure build completed successfully (green checkmark)
2. Click on workflow run
3. Scroll to bottom
4. Click artifact name to download

### .exe Too Large (>50MB)
**Fix:** Normal for Python apps with PyQt5. 25-30MB is expected.

---

## 🎯 Summary

**Easiest Method: GitHub Actions**

```bash
# One-time setup:
1. Create GitHub repo
2. Add workflow file
3. Push code

# Result:
Every push → Automatic build → Download .exe

# For releases:
git tag v1.0.0
git push origin v1.0.0
→ Creates downloadable release
```

**No Windows PC needed! 🎉**

---

Created: November 30, 2025
Platform: GitHub Actions (Free)
Build Time: ~5 minutes
Output: Windows .exe (25-30MB)

============================================
