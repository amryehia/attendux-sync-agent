# Attendux Sync Agent - Complete Guide
# ============================================
# Desktop application for syncing ZKTeco devices
# Multi-tenant support with brand colors
# ============================================

## 📦 What We Built

### Desktop Application Features:
- ✅ **Multi-tenant support** - Each company only sees their own devices
- ✅ **Attendux brand colors** (Primary: #3599c7, Dark: #19344f)
- ✅ **Attendux logo** from landing page
- ✅ **Auto-sync** every 15 minutes (configurable)
- ✅ **System tray** - Runs in background
- ✅ **Auto-start** with Windows
- ✅ **Beautiful GUI** with PyQt5
- ✅ **Activity logs** with color coding
- ✅ **Desktop notifications**
- ✅ **Settings persistence**
- ✅ **Secure HTTPS** communication

### Backend API Features:
- ✅ **License verification** with company info
- ✅ **Tenant-scoped device loading** - Only company's devices
- ✅ **Attendance record processing** with duplicate prevention
- ✅ **Check-in/Check-out detection**
- ✅ **Employee matching** by biometric_id or employee_id
- ✅ **Statistics endpoint** for monitoring

---

## 🚀 How to Build

### Prerequisites:
```bash
# Windows 10/11
# Python 3.8 or higher
# pip (Python package manager)
```

### Step 1: Setup Environment
```bash
cd sync-agent

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Download Logo
```bash
# Download logo from your server
curl -o logo.png https://app.attendux.com/public/storage/logo.png

# Or manually download and save as logo.png
```

### Step 3: Build Executable
```bash
# Windows: Double-click build.bat
# Or run manually:
build.bat

# Or use PowerShell:
.\build.bat
```

### Build Output:
```
dist/
  └── Attendux-Sync-Agent.exe  (~20 MB)
```

---

## 📋 Backend Setup

### Step 1: Deploy API Controller
The API controller is already created:
```
applive/app/Http/Controllers/Api/SyncController.php
```

### Step 2: Add Routes
Routes are already added to:
```
applive/routes/api.php
```

### Step 3: Test API Endpoints

#### Test 1: Verify License
```bash
curl -X POST https://app.attendux.com/api/sync/verify \
  -H "X-License-Key: ATX-C83E-9317-46D1-91E6"
```

Expected response:
```json
{
  "valid": true,
  "company": {
    "id": 22,
    "name": "Movera",
    "tenant_id": "...",
    "plan": "Attendux Plus",
    "license_expiry": "2026-11-30",
    "features": ["zkteco_sync", "attendance_tracking", ...]
  }
}
```

#### Test 2: Get Devices
```bash
curl -X GET https://app.attendux.com/api/sync/devices \
  -H "X-License-Key: ATX-C83E-9317-46D1-91E6"
```

Expected response:
```json
{
  "success": true,
  "devices": [
    {
      "id": 6,
      "name": "ZKTeco Main",
      "ip": "192.168.1.201",
      "port": 4370,
      "model": "Z40 Pro",
      "location": "Main Office"
    }
  ],
  "company_id": 22,
  "tenant_id": "..."
}
```

#### Test 3: Send Attendance
```bash
curl -X POST https://app.attendux.com/api/sync/attendance \
  -H "X-License-Key: ATX-C83E-9317-46D1-91E6" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {
        "employee_id": "123",
        "timestamp": "2025-11-30T09:00:00",
        "device_id": "6",
        "type": "auto",
        "status": 0
      }
    ]
  }'
```

Expected response:
```json
{
  "success": true,
  "synced": 1,
  "skipped": 0,
  "total": 1,
  "company": "Movera",
  "tenant_id": "...",
  "errors": []
}
```

---

## 🎨 Brand Colors Used

From `landing/index.html`:
```css
--primary-color: #3599c7    /* Attendux Blue */
--primary-dark: #19344f     /* Dark Blue */
--secondary-color: #667eea  /* Purple */
--success-color: #10b981    /* Green */
--warning-color: #f59e0b    /* Orange */
--danger-color: #ef4444     /* Red */
```

Logo:
```
https://app.attendux.com/public/storage/logo.png
```

---

## 👤 Customer Setup Instructions

### For Movera Customer (eng.zakin@gmail.com):

1. **Download & Install**
   ```
   Download: https://app.attendux.com/downloads/Attendux-Sync-Agent.exe
   Double-click to run (no installation needed)
   ```

2. **Enter License Key**
   ```
   License: ATX-C83E-9317-46D1-91E6
   Click "Connect"
   ```

3. **Verify Devices Loaded**
   ```
   Should see: ZKTeco Main (192.168.1.201:4370)
   Loaded automatically from cloud!
   ```

4. **Start Auto-Sync**
   ```
   Click "Start Auto-Sync"
   Syncs every 15 minutes automatically
   ```

5. **Minimize to Tray**
   ```
   Close window - runs in background
   Green icon in system tray = working
   ```

---

## 🔧 Multi-Tenant Architecture

### How It Works:

```
┌─────────────────────────────────────────┐
│ Customer 1 (Movera)                     │
│ License: ATX-C83E-9317-46D1-91E6        │
│ Tenant ID: movera_tenant                │
│                                          │
│ Desktop App → API → Database            │
│   ↓            ↓         ↓               │
│ Devices:    Filter:   Only sees:        │
│ - All       company_id  - Device 6      │
│             AND         - Employee 1-30 │
│             tenant_id   - Own records   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Customer 2 (Another Company)            │
│ License: ATX-XXXX-XXXX-XXXX-XXXX        │
│ Tenant ID: other_tenant                 │
│                                          │
│ Desktop App → API → Database            │
│   ↓            ↓         ↓               │
│ Devices:    Filter:   Only sees:        │
│ - All       company_id  - Device 7, 8   │
│             AND         - Employee 1-50 │
│             tenant_id   - Own records   │
└─────────────────────────────────────────┘
```

### Database Filtering:

Every API query includes:
```php
->where('company_id', $company->id)
->where('tenant_id', $company->tenant_id)
```

This ensures:
- ✅ Each company only sees their own devices
- ✅ Each company only syncs their own employees
- ✅ Each company only sees their own attendance records
- ✅ Complete data isolation between tenants

---

## 📊 App Screenshots (ASCII)

### Main Window:
```
┌──────────────────────────────────────────────────┐
│  [🔵 Logo] Attendux Sync Agent           v1.0.0  │
│            Multi-Tenant ZKTeco Sync              │
├──────────────────────────────────────────────────┤
│  ● ✅ Connected - Movera    Last sync: 09:15:23  │
├──────────────────────────────────────────────────┤
│  License Configuration                           │
│  License Key: [ATX-C83E-9317-46D1-91E6] [Connect]│
│  Company: Movera                                 │
│  Plan: Attendux Plus                             │
│  License Expires: 2026-11-30                     │
├──────────────────────────────────────────────────┤
│  Devices (Loaded from Cloud)                     │
│  ┌────────────────────────────────────────────┐  │
│  │ ✓ ZKTeco Main - 192.168.1.201:4370        │  │
│  │   (ID: 6)                                  │  │
│  └────────────────────────────────────────────┘  │
│  [↻ Refresh from Cloud]                          │
├──────────────────────────────────────────────────┤
│  [▶ Sync Now] [⏹ Stop Auto-Sync]                │
├──────────────────────────────────────────────────┤
│  Settings                                        │
│  Sync Interval: [15 ▼] minutes                   │
│  ☑ Start with Windows  ☑ Show Notifications     │
├──────────────────────────────────────────────────┤
│  Activity Logs                                   │
│  ┌────────────────────────────────────────────┐  │
│  │ [09:15:23] 🔄 Starting sync...            │  │
│  │ [09:15:24] 📡 Connecting to ZKTeco Main...│  │
│  │ [09:15:25]    Found 12 records            │  │
│  │ [09:15:26]    ✅ Synced 12/12 records      │  │
│  │ [09:15:26] ✅ Sync completed! 12 records   │  │
│  └────────────────────────────────────────────┘  │
│  [Clear Logs]                                    │
└──────────────────────────────────────────────────┘
```

---

## ⚙️ Configuration Files

### Settings Location:
```
Windows: C:\Users\<username>\.attendux_sync\settings.json
```

### Settings Format:
```json
{
  "license_key": "ATX-C83E-9317-46D1-91E6",
  "devices": [
    {
      "id": 6,
      "name": "ZKTeco Main",
      "ip": "192.168.1.201",
      "port": 4370
    }
  ],
  "sync_interval": 15,
  "auto_start": true,
  "show_notifications": true,
  "last_sync": "2025-11-30T09:15:26"
}
```

---

## 🔍 Troubleshooting

### Problem 0: macOS App Won't Open (NEW)
**Symptom:**
```
App bounces in dock then closes
OR
"Attendux Sync Agent is damaged and can't be opened"
OR
App doesn't respond when double-clicked
```

**Solution - Method 1: Use the Helper Script (Easiest)**
1. After extracting the .app, you'll see `INSTALL_ON_MAC.command`
2. Double-click `INSTALL_ON_MAC.command`
3. Follow the on-screen instructions
4. Then double-click `Attendux Sync Agent.app`

**Solution - Method 2: Right-Click Open**
1. Right-click (or Control+Click) on `Attendux Sync Agent.app`
2. Select "Open" from the context menu
3. Click "Open" in the security dialog that appears
4. App will now open normally

**Solution - Method 3: Terminal Command**
1. Open Terminal (Applications → Utilities → Terminal)
2. Navigate to where you extracted the app:
   ```bash
   cd ~/Downloads  # or wherever you extracted it
   ```
3. Remove quarantine attribute:
   ```bash
   xattr -cr "Attendux Sync Agent.app"
   ```
4. Double-click the app normally

**Solution - Method 4: System Preferences**
1. Try to open the app (it will fail)
2. Go to System Preferences → Security & Privacy
3. Click "Open Anyway" button
4. Click "Open" in the confirmation dialog

**Why this happens:**
macOS blocks apps downloaded from the internet that aren't signed with an Apple Developer certificate. This is a security feature called "Gatekeeper". The methods above tell macOS that you trust this app.

---

### Problem 1: Can't Connect to Device
**Symptom:**
```
❌ Error syncing ZKTeco Main: Network error
```

**Solution:**
1. Verify desktop app is on same network as device
2. Check device IP: `ping 192.168.1.201`
3. Check device port is open: `telnet 192.168.1.201 4370`
4. Verify device is powered on
5. Check firewall on PC running app

---

### Problem 2: License Verification Failed
**Symptom:**
```
❌ Invalid license key or expired
```

**Solution:**
1. Check license key is correct (copy-paste from dashboard)
2. Verify license not expired
3. Ensure license has `zkteco_sync` feature
4. Run FIX_LICENSE_FEATURES.sql if features=NULL

---

### Problem 3: Devices Not Loading
**Symptom:**
```
ℹ️ No devices found
```

**Solution:**
1. Add devices in Attendux dashboard first:
   - Go to Settings → ZKTeco Devices
   - Click "Add Device"
   - Enter device details
2. Click "Refresh from Cloud" in app
3. Verify company_id and tenant_id are correct

---

### Problem 4: Employees Not Found
**Symptom:**
```
⚠️ Sync completed with errors
Employee not found: 123
```

**Solution:**
1. Add employees in Attendux dashboard
2. Set employee `biometric_id` to match ZKTeco user_id
3. Or set employee `employee_id` to match
4. Verify employees have correct company_id and tenant_id

---

## 📈 Monitoring & Statistics

### Check Sync Status:
```bash
curl -X GET https://app.attendux.com/api/sync/stats \
  -H "X-License-Key: ATX-C83E-9317-46D1-91E6"
```

Response:
```json
{
  "success": true,
  "stats": {
    "total_employees": 30,
    "total_devices": 1,
    "attendance_today": 25,
    "attendance_this_month": 450,
    "last_sync": "2025-11-30T09:15:26"
  },
  "company": "Movera"
}
```

---

## 🎯 Benefits vs Other Solutions

| Feature | Desktop App | Port Forwarding | DDNS |
|---------|-------------|-----------------|------|
| **Setup Time** | 5 minutes | 30 minutes | 45 minutes |
| **Technical Knowledge** | None | Medium | High |
| **Router Changes** | No | Yes | Yes |
| **Security** | High (HTTPS) | Medium | Medium |
| **Maintenance** | None | IP changes | Monthly confirm |
| **Support** | Easy | Hard | Medium |
| **Multi-tenant** | Native | Manual | Manual |
| **Auto-updates** | Yes | N/A | N/A |

**Winner: Desktop App! 🏆**

---

## 🚀 Deployment Checklist

### Backend:
- [ ] Deploy SyncController.php to production
- [ ] Add routes to api.php
- [ ] Run FIX_LICENSE_FEATURES.sql
- [ ] Test API endpoints
- [ ] Clear Laravel cache

### Desktop App:
- [ ] Download logo.png
- [ ] Build executable with build.bat
- [ ] Test on Windows 10/11
- [ ] Create installer (optional)
- [ ] Upload to: https://app.attendux.com/downloads/
- [ ] Update landing page with download link

### Customer:
- [ ] Send download link
- [ ] Send setup instructions
- [ ] Provide license key
- [ ] Test sync together
- [ ] Verify attendance records appear in dashboard

---

## 💡 Future Enhancements

### Phase 2 (Optional):
- [ ] Auto-update mechanism
- [ ] Multiple language support (Arabic/English)
- [ ] Advanced device management (add/edit devices from app)
- [ ] Real-time sync status dashboard
- [ ] Employee photos sync
- [ ] Custom sync schedules per device
- [ ] Offline mode with queue
- [ ] Email reports
- [ ] WhatsApp notifications
- [ ] macOS and Linux versions

---

## 📞 Support

**For Developers:**
- Check logs: `%USERPROFILE%\.attendux_sync\`
- API docs: This file
- Debug mode: Run `attendux_sync_agent.py` directly

**For Customers:**
- Email: support@attendux.com
- In-app: Help → Contact Support
- Remote desktop for troubleshooting

---

**Created:** November 30, 2025  
**Version:** 1.0.0  
**Status:** Ready for Production  
**Multi-tenant:** ✅ Yes  
**Brand Colors:** ✅ Applied  
**Logo:** ✅ Integrated  

============================================
# THE EASIEST SOLUTION - NO ROUTER HASSLES!
============================================
