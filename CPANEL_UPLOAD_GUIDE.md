# 📤 cPanel Upload Guide - Exact Files & Paths
# ============================================

## 🎯 FILES TO UPLOAD TO CPANEL

### ✅ PART 1: Backend API Files

#### File 1: API Controller
```
LOCAL PATH:
/Applications/XAMPP/xamppfiles/htdocs/payroll-attendance/applive/app/Http/Controllers/Api/SyncController.php

CPANEL PATH:
/public_html/applive/app/Http/Controllers/Api/SyncController.php

HOW:
1. Open cPanel File Manager
2. Navigate to: public_html/applive/app/Http/Controllers/Api/
3. If "Api" folder doesn't exist, create it
4. Upload: SyncController.php
```

#### File 2: API Routes
```
LOCAL PATH:
/Applications/XAMPP/xamppfiles/htdocs/payroll-attendance/applive/routes/api.php

CPANEL PATH:
/public_html/applive/routes/api.php

HOW:
1. Navigate to: public_html/applive/routes/
2. BACKUP existing api.php first! (Download it)
3. Edit existing api.php
4. Add the new routes from our file
```

**IMPORTANT:** Don't replace the entire api.php file! Only ADD the new routes:
```php
// Add these routes to existing api.php:
Route::prefix('sync')->group(function () {
    Route::post('/verify', [SyncController::class, 'verifyLicense']);
    Route::get('/devices', [SyncController::class, 'getDevices']);
    Route::post('/attendance', [SyncController::class, 'receiveAttendance']);
    Route::get('/stats', [SyncController::class, 'getStats']);
});
```

---

### ✅ PART 2: Desktop App (EXE File)

#### File 3: Windows Executable
```
LOCAL PATH:
Download from GitHub Actions:
https://github.com/amryehia/attendux-sync-agent/actions
(After build completes, download artifact)

CPANEL PATH:
/public_html/applive/public/downloads/Attendux-Sync-Agent.exe

HOW:
1. Wait for GitHub build to complete (~5 minutes)
2. Download artifact from GitHub Actions
3. Extract: Attendux-Sync-Agent.exe
4. Upload to cPanel:
   - Navigate to: public_html/applive/public/downloads/
   - If "downloads" folder doesn't exist, create it
   - Upload: Attendux-Sync-Agent.exe
   - Set permissions: 644 (read for everyone)
```

**Download URL will be:**
```
https://app.attendux.com/downloads/Attendux-Sync-Agent.exe
```

---

## 📋 COMPLETE UPLOAD CHECKLIST

### Step 1: Upload API Controller ✅
```
File: SyncController.php
From: /Applications/XAMPP/.../applive/app/Http/Controllers/Api/
To:   /public_html/applive/app/Http/Controllers/Api/
Size: ~15 KB
```

### Step 2: Update API Routes ✅
```
File: api.php
Edit: /public_html/applive/routes/api.php
Action: Add new sync routes (don't replace entire file!)
```

### Step 3: Upload EXE ✅
```
File: Attendux-Sync-Agent.exe
From: GitHub Actions artifact (download first)
To:   /public_html/applive/public/downloads/
Size: ~25-30 MB
```

### Step 4: Clear Laravel Cache ✅
```
Method 1 (cPanel Terminal):
cd /public_html/applive
php artisan cache:clear
php artisan config:clear
php artisan route:clear

Method 2 (SSH):
ssh user@app.attendux.com
cd /public_html/applive
php artisan cache:clear
php artisan config:clear
php artisan route:clear

Method 3 (Create PHP file in browser):
Create: /public_html/applive/public/clear-cache.php
Content:
<?php
require __DIR__.'/../vendor/autoload.php';
$app = require_once __DIR__.'/../bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->call('cache:clear');
$kernel->call('config:clear');
$kernel->call('route:clear');
echo "Cache cleared!";

Visit: https://app.attendux.com/clear-cache.php
Then delete the file!
```

---

## 🔍 VERIFICATION STEPS

### Test 1: API Controller Exists
```
Check in cPanel File Manager:
/public_html/applive/app/Http/Controllers/Api/SyncController.php

Should exist and be ~15 KB
```

### Test 2: Routes Work
```
Open in browser:
https://app.attendux.com/api/sync/verify

You should see either:
- JSON error (means route works!)
- Or 404 (means route not added yet)
```

### Test 3: EXE Downloadable
```
Open in browser:
https://app.attendux.com/downloads/Attendux-Sync-Agent.exe

Should download the file (~25-30 MB)
```

### Test 4: API Endpoints
```bash
# Test license verification
curl -X POST https://app.attendux.com/api/sync/verify \
  -H "X-License-Key: ATX-C83E-9317-46D1-91E6"

# Should return:
# {"valid":true,"company":{...}}
```

---

## 📂 FOLDER STRUCTURE IN CPANEL

```
public_html/
└── applive/
    ├── app/
    │   └── Http/
    │       └── Controllers/
    │           └── Api/
    │               └── SyncController.php  ← Upload here
    ├── routes/
    │   └── api.php  ← Edit this (add routes)
    └── public/
        └── downloads/
            └── Attendux-Sync-Agent.exe  ← Upload here
```

---

## 🎯 QUICK REFERENCE

### Upload via cPanel File Manager:

1. **Login to cPanel**
   - URL: https://app.attendux.com:2083
   - Or your hosting control panel

2. **Open File Manager**
   - Click "File Manager"
   - Navigate to public_html/applive/

3. **Create Folders (if needed)**
   - app/Http/Controllers/Api/ (for SyncController.php)
   - public/downloads/ (for .exe file)

4. **Upload Files**
   - Click "Upload" button
   - Select files
   - Wait for upload to complete

5. **Set Permissions**
   - Right-click files
   - "Change Permissions"
   - Files: 644
   - Folders: 755

---

## 🆘 TROUBLESHOOTING

### Problem: "Api folder doesn't exist"
**Solution:**
```
1. Navigate to: public_html/applive/app/Http/Controllers/
2. Click "New Folder"
3. Name: Api
4. Upload SyncController.php inside it
```

### Problem: "downloads folder doesn't exist"
**Solution:**
```
1. Navigate to: public_html/applive/public/
2. Click "New Folder"
3. Name: downloads
4. Upload Attendux-Sync-Agent.exe inside it
```

### Problem: "Can't upload large file (30MB)"
**Solution:**
```
Option 1: Use cPanel Upload (usually allows up to 50MB)
Option 2: Use FTP client (FileZilla)
Option 3: Upload via SSH/SCP
Option 4: Split upload or compress
```

### Problem: "Routes not working"
**Solution:**
```
1. Make sure you ADDED routes, not replaced entire api.php
2. Clear cache:
   cd /public_html/applive
   php artisan route:clear
3. Check routes:
   php artisan route:list | grep sync
```

---

## 📊 FILE SIZES (Approximate)

| File | Size | Upload Time (10 Mbps) |
|------|------|------------------------|
| SyncController.php | 15 KB | 1 second |
| api.php changes | 1 KB | 1 second |
| Attendux-Sync-Agent.exe | 25-30 MB | 20-25 seconds |

**Total Upload:** < 30 seconds

---

## ✅ AFTER UPLOAD

### 1. Test API
```bash
curl -X POST https://app.attendux.com/api/sync/verify \
  -H "X-License-Key: ATX-C83E-9317-46D1-91E6"
```

### 2. Test Download
```
https://app.attendux.com/downloads/Attendux-Sync-Agent.exe
```

### 3. Send to Customer
```
Hi [Customer],

Your Attendux Sync Agent is ready!

Download: https://app.attendux.com/downloads/Attendux-Sync-Agent.exe
License: ATX-C83E-9317-46D1-91E6

Setup (2 minutes):
1. Download and run the file
2. Enter your license key
3. Click "Connect"
4. Click "Start Auto-Sync"
5. Done!

No router configuration needed!

Support: support@attendux.com
```

---

## 🎉 SUMMARY

**3 Files to Upload:**
1. ✅ SyncController.php → `/public_html/applive/app/Http/Controllers/Api/`
2. ✅ api.php (edit) → `/public_html/applive/routes/`
3. ✅ Attendux-Sync-Agent.exe → `/public_html/applive/public/downloads/`

**Then:**
4. ✅ Clear Laravel cache
5. ✅ Test API endpoints
6. ✅ Test .exe download
7. ✅ Send to customer!

**Total Time:** 10-15 minutes

---

Created: November 30, 2025
Target: cPanel on app.attendux.com
Status: Ready to upload
Next: Wait for GitHub build, then upload!

============================================
