#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Attendux Sync Agent
Desktop application for syncing ZKTeco devices with Attendux cloud
Multi-tenant support - each company syncs only their own devices
"""

import sys
import json
import os
import requests
import platform
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

# Try to import QWebEngineView, but make it optional for Windows
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    print("Warning: QtWebEngine not available. Dashboard will open in external browser.")

# Platform-specific startup imports
PLATFORM = platform.system()

if PLATFORM == 'Windows':
    try:
        import winreg as reg
        WINDOWS_STARTUP_AVAILABLE = True
    except ImportError:
        WINDOWS_STARTUP_AVAILABLE = False
else:
    WINDOWS_STARTUP_AVAILABLE = False

# macOS uses plist files for login items
MACOS_STARTUP_AVAILABLE = (PLATFORM == 'Darwin')

# Try to import ZK library, but make it optional for building
try:
    from zk import ZK
    ZK_AVAILABLE = True
except ImportError:
    ZK_AVAILABLE = False
    print("Warning: ZK library not available. Install with: pip install pyzk")

# Brand Colors (from landing/index.html)
BRAND_PRIMARY = "#3599c7"
BRAND_PRIMARY_DARK = "#19344f"
BRAND_SECONDARY = "#667eea"
BRAND_SUCCESS = "#10b981"
BRAND_WARNING = "#f59e0b"
BRAND_DANGER = "#ef4444"
BRAND_WHITE = "#ffffff"
BRAND_GRAY_100 = "#f3f4f6"
BRAND_GRAY_800 = "#1f2937"

# API Configuration
API_BASE_URL = "https://app.attendux.com/api/sync"
LOGO_URL = "https://app.attendux.com/public/storage/logo.png"

# Settings file
SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".attendux_sync", "settings.json")

# Translations
TRANSLATIONS = {
    'ar': {
        'app_title': 'أتندوكس',
        'app_subtitle': 'مزامنة أجهزة البصمة متعددة المستأجرين',
        'version': 'الإصدار',
        'license_key': 'مفتاح الترخيص',
        'license_placeholder': 'أدخل مفتاح الترخيص الخاص بك',
        'connect': 'اتصال',
        'disconnect': 'قطع الاتصال',
        'company': 'الشركة',
        'license_status': 'حالة الترخيص',
        'valid_until': 'صالح حتى',
        'plan': 'الخطة',
        'devices': 'الأجهزة',
        'no_devices': 'لم يتم العثور على أجهزة',
        'start_sync': 'بدء المزامنة',
        'stop_sync': 'إيقاف المزامنة',
        'open_dashboard': 'فتح لوحة التحكم',
        'settings': 'الإعدادات',
        'sync_interval': 'فترة المزامنة (دقائق)',
        'auto_sync': 'مزامنة تلقائية',
        'startup': 'بدء مع النظام',
        'notifications': 'إشعارات',
        'logs': 'السجلات',
        'clear_logs': 'مسح السجلات',
        'status_connected': 'متصل',
        'status_disconnected': 'غير متصل',
        'invalid_license': 'ترخيص غير صالح',
        'connecting': 'جاري الاتصال...',
        'syncing': 'جاري المزامنة...',
        'sync_completed': 'اكتملت المزامنة',
        'language': 'اللغة',
        'arabic': 'العربية',
        'english': 'الإنجليزية',
        'back': 'رجوع',
        'forward': 'التالي',
        'refresh': 'تحديث',
        'close': 'إغلاق',
        'not_connected': 'غير متصل',
        'last_sync_never': 'آخر مزامنة: أبداً',
        'last_sync': 'آخر مزامنة',
        'license_configuration': 'إعدادات الترخيص',
        'devices_cloud': 'الأجهزة (محملة من السحابة)',
        'refresh_from_cloud': '↻ تحديث من السحابة',
        'sync_now': '▶ مزامنة الآن',
        'start_auto_sync': '⏱ بدء المزامنة التلقائية',
        'stop_auto_sync': '⏹ إيقاف المزامنة التلقائية',
        'activity_logs': 'سجل النشاط',
        'show': 'عرض',
        'quit': 'خروج',
        'connected': 'متصل',
        'minutes': 'دقائق',
        'company_label': 'الشركة',
        'plan_label': 'الخطة',
        'license_expires': 'انتهاء الترخيص'
    },
    'en': {
        'app_title': 'Attendux',
        'app_subtitle': 'Multi-Tenant ZKTeco Device Synchronization',
        'version': 'Version',
        'license_key': 'License Key',
        'license_placeholder': 'Enter your license key',
        'connect': 'Connect',
        'disconnect': 'Disconnect',
        'company': 'Company',
        'license_status': 'License Status',
        'valid_until': 'Valid Until',
        'plan': 'Plan',
        'devices': 'Devices',
        'no_devices': 'No devices found',
        'start_sync': 'Start Sync',
        'stop_sync': 'Stop Sync',
        'open_dashboard': 'Open Dashboard',
        'settings': 'Settings',
        'sync_interval': 'Sync Interval (minutes)',
        'auto_sync': 'Auto Sync',
        'startup': 'Start with System',
        'notifications': 'Notifications',
        'logs': 'Logs',
        'clear_logs': 'Clear Logs',
        'status_connected': 'Connected',
        'status_disconnected': 'Disconnected',
        'invalid_license': 'Invalid License',
        'connecting': 'Connecting...',
        'syncing': 'Syncing...',
        'sync_completed': 'Sync Completed',
        'language': 'Language',
        'arabic': 'العربية',
        'english': 'English',
        'back': 'Back',
        'forward': 'Forward',
        'refresh': 'Refresh',
        'close': 'Close',
        'not_connected': 'Not Connected',
        'last_sync_never': 'Last sync: Never',
        'last_sync': 'Last sync',
        'license_configuration': 'License Configuration',
        'devices_cloud': 'Devices (Loaded from Cloud)',
        'refresh_from_cloud': '↻ Refresh from Cloud',
        'sync_now': '▶ Sync Now',
        'start_auto_sync': '⏱ Start Auto-Sync',
        'stop_auto_sync': '⏹ Stop Auto-Sync',
        'activity_logs': 'Activity Logs',
        'show': 'Show',
        'quit': 'Quit',
        'connected': 'Connected',
        'minutes': 'minutes',
        'company_label': 'Company',
        'plan_label': 'Plan',
        'license_expires': 'License Expires'
    }
}


class SettingsManager:
    """Manage app settings"""
    
    @staticmethod
    def load():
        """Load settings from file"""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'license_key': '',
            'devices': [],
            'sync_interval': 15,
            'auto_start': True,
            'show_notifications': True,
            'last_sync': None,
            'language': 'ar'  # Arabic as default
        }
    
    @staticmethod
    def save(settings):
        """Save settings to file"""
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)


class AttenduxAPI:
    """Handle API communication with Attendux cloud"""
    
    def __init__(self, license_key):
        self.license_key = license_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-License-Key': license_key,
            'Content-Type': 'application/json',
            'User-Agent': 'Attendux-Sync-Agent/1.0'
        })
    
    def verify_license(self):
        """Verify license key and get company info"""
        try:
            response = self.session.post(
                f"{API_BASE_URL}/verify",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"License verification error: {e}")
            return None
    
    def get_company_devices(self):
        """Get all devices for this company (tenant)"""
        try:
            response = self.session.get(
                f"{API_BASE_URL}/devices",
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get('devices', [])
            return []
        except Exception as e:
            print(f"Get devices error: {e}")
            return []
    
    def send_attendance(self, records):
        """Send attendance records to cloud"""
        try:
            response = self.session.post(
                f"{API_BASE_URL}/attendance",
                json={'records': records},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Send attendance error: {e}")
            return None


class SyncWorker(QThread):
    """Background worker for syncing devices"""
    
    # Signals
    log_signal = pyqtSignal(str, str)  # message, level (info/success/error)
    progress_signal = pyqtSignal(int, int)  # current, total
    sync_complete_signal = pyqtSignal(dict)  # result stats
    
    def __init__(self, api, devices):
        super().__init__()
        self.api = api
        self.devices = devices
        self.is_running = True
    
    def run(self):
        """Run sync process"""
        total_synced = 0
        total_records = 0
        errors = []
        
        self.log_signal.emit("🔄 Starting sync...", "info")
        
        for idx, device in enumerate(self.devices):
            if not self.is_running:
                break
            
            self.progress_signal.emit(idx + 1, len(self.devices))
            
            try:
                # Check if ZK library is available
                if not ZK_AVAILABLE:
                    error = f"ZK library not installed. Cannot sync {device['name']}"
                    errors.append(error)
                    self.log_signal.emit(f"   ❌ {error}", "error")
                    continue
                
                # Connect to device
                self.log_signal.emit(f"📡 Connecting to {device['name']} ({device['ip']}:{device['port']})...", "info")
                
                zk = ZK(device['ip'], port=int(device['port']), timeout=5)
                conn = zk.connect()
                
                # Get attendance records
                attendances = conn.get_attendance()
                self.log_signal.emit(f"   Found {len(attendances)} records", "info")
                
                if len(attendances) > 0:
                    # Prepare records
                    records = []
                    for att in attendances:
                        records.append({
                            'employee_id': str(att.user_id),
                            'timestamp': att.timestamp.isoformat(),
                            'device_id': device.get('id', device['name']),
                            'type': 'auto',
                            'status': att.status if hasattr(att, 'status') else 1
                        })
                    
                    # Send to cloud
                    result = self.api.send_attendance(records)
                    
                    if result and result.get('success'):
                        synced = result.get('synced', 0)
                        total_synced += synced
                        total_records += len(records)
                        self.log_signal.emit(f"   ✅ Synced {synced}/{len(records)} records", "success")
                    else:
                        error = f"Failed to sync {device['name']}"
                        errors.append(error)
                        self.log_signal.emit(f"   ❌ {error}", "error")
                else:
                    self.log_signal.emit(f"   ℹ️ No new records", "info")
                
                conn.disconnect()
                
            except Exception as e:
                error = f"Error syncing {device['name']}: {str(e)}"
                errors.append(error)
                self.log_signal.emit(f"   ❌ {error}", "error")
        
        # Complete
        result = {
            'total_synced': total_synced,
            'total_records': total_records,
            'devices_count': len(self.devices),
            'errors': errors,
            'timestamp': datetime.now().isoformat()
        }
        
        if len(errors) == 0:
            self.log_signal.emit(f"✅ Sync completed! {total_synced} records synced", "success")
        else:
            self.log_signal.emit(f"⚠️ Sync completed with {len(errors)} errors", "warning")
        
        self.sync_complete_signal.emit(result)
    
    def stop(self):
        """Stop sync process"""
        self.is_running = False


class AttenduxSyncAgent(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager.load()
        self.current_language = self.settings.get('language', 'ar')
        self.api = None
        self.company_info = None
        self.sync_worker = None
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.start_sync)
        self.dashboard_browser = None
        
        # Set initial layout direction based on language
        if self.current_language == 'ar':
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)
        
        self.init_ui()
        self.update_ui_language()
        
        # Defer heavy operations to avoid blocking UI on startup
        # Load logo asynchronously after UI is shown
        QTimer.singleShot(500, self.load_logo_async)
        
        # Auto-connect if license key exists (defer to avoid blocking)
        if self.settings.get('license_key'):
            QTimer.singleShot(2000, self.auto_connect)
    
    def tr(self, key):
        """Translate key to current language"""
        return TRANSLATIONS.get(self.current_language, TRANSLATIONS['ar']).get(key, key)
    
    def switch_language(self, lang_code):
        """Switch application language"""
        # Save the language first
        self.current_language = lang_code
        self.settings['language'] = lang_code
        SettingsManager.save(self.settings)
        
        # Show message that user needs to restart manually
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        if lang_code == 'ar':
            msg.setWindowTitle("تم حفظ اللغة")
            msg.setText("تم حفظ تفضيل اللغة بنجاح.")
            msg.setInformativeText("الرجاء إعادة تشغيل التطبيق يدوياً لتطبيق التغيير.")
        else:
            msg.setWindowTitle("Language Saved")
            msg.setText("Language preference saved successfully.")
            msg.setInformativeText("Please restart the application manually to apply the change.")
        msg.exec_()
    
    def update_ui_language(self):
        """Update all UI elements with current language"""
        self.setWindowTitle(self.tr('app_title'))
        # Update all translatable UI elements
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(self.tr('app_subtitle'))
        if hasattr(self, 'status_label') and self.tr('not_connected') in self.status_label.text():
            self.status_label.setText(self.tr('not_connected'))
        if hasattr(self, 'last_sync_label') and self.tr('last_sync_never') in self.last_sync_label.text():
            self.last_sync_label.setText(self.tr('last_sync_never'))
        if hasattr(self, 'license_group'):
            self.license_group.setTitle(self.tr('license_configuration'))
        if hasattr(self, 'license_label'):
            self.license_label.setText(self.tr('license_key') + ":")
        if hasattr(self, 'license_input'):
            self.license_input.setPlaceholderText(self.tr('license_placeholder'))
        if hasattr(self, 'connect_btn'):
            self.connect_btn.setText(self.tr('connect'))
        if hasattr(self, 'devices_group'):
            self.devices_group.setTitle(self.tr('devices_cloud'))
        if hasattr(self, 'refresh_devices_btn'):
            self.refresh_devices_btn.setText(self.tr('refresh_from_cloud'))
        if hasattr(self, 'dashboard_btn'):
            self.dashboard_btn.setText(self.tr('open_dashboard'))
        if hasattr(self, 'sync_now_btn'):
            self.sync_now_btn.setText(self.tr('sync_now'))
        if hasattr(self, 'start_sync_btn'):
            current_text = self.start_sync_btn.text()
            if self.tr('start_auto_sync') in current_text or 'Start' in current_text:
                self.start_sync_btn.setText(self.tr('start_auto_sync'))
            else:
                self.start_sync_btn.setText(self.tr('stop_auto_sync'))
        if hasattr(self, 'settings_group'):
            self.settings_group.setTitle(self.tr('settings'))
        if hasattr(self, 'sync_interval_label'):
            self.sync_interval_label.setText(self.tr('sync_interval') + ":")
        if hasattr(self, 'interval_spinbox'):
            self.interval_spinbox.setSuffix(" " + self.tr('minutes'))
        if hasattr(self, 'startup_checkbox'):
            self.startup_checkbox.setText(self.tr('startup'))
        if hasattr(self, 'notifications_checkbox'):
            self.notifications_checkbox.setText(self.tr('notifications'))
        if hasattr(self, 'logs_group'):
            self.logs_group.setTitle(self.tr('activity_logs'))
        if hasattr(self, 'clear_logs_btn'):
            self.clear_logs_btn.setText(self.tr('clear_logs'))
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(self.tr('app_title'))
        self.setMinimumSize(1100, 800)
        
        self.setStyleSheet(self.get_stylesheet())
        
        # Start maximized for better display
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(
            (screen.width() - 1100) // 2,
            (screen.height() - 800) // 2,
            1100, 800
        )
        self.showMaximized()  # Start maximized to avoid cropped fields
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with logo
        self.create_header(main_layout)
        
        # Status section
        self.create_status_section(main_layout)
        
        # License section
        self.create_license_section(main_layout)
        
        # Devices section
        self.create_devices_section(main_layout)
        
        # Control buttons
        self.create_control_buttons(main_layout)
        
        # Settings section
        self.create_settings_section(main_layout)
        
        # Logs section
        self.create_logs_section(main_layout)
        
        # System tray
        self.create_system_tray()
    
    def create_header(self, layout):
        """Create header with logo"""
        header_widget = QWidget()
        header_widget.setObjectName("header")
        header_layout = QHBoxLayout(header_widget)
        
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(60, 60)
        self.logo_label.setScaledContents(True)
        header_layout.addWidget(self.logo_label)
        
        # Title
        title_layout = QVBoxLayout()
        self.title_label = QLabel(self.tr('app_title'))
        self.title_label.setObjectName("title")
        self.title_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {BRAND_PRIMARY_DARK};")
        self.subtitle_label = QLabel(self.tr('app_subtitle'))
        self.subtitle_label.setStyleSheet(f"font-size: 12px; color: #666;")
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)
        header_layout.addLayout(title_layout)
        
        header_layout.addStretch()
        
        # Language Switcher
        lang_widget = QWidget()
        lang_layout = QHBoxLayout(lang_widget)
        lang_layout.setContentsMargins(0, 0, 0, 0)
        lang_layout.setSpacing(5)
        
        lang_label = QLabel(self.tr('language') + ":")
        lang_label.setStyleSheet("font-size: 11px; color: #666;")
        lang_layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("العربية", "ar")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.setCurrentIndex(0 if self.current_language == 'ar' else 1)
        self.lang_combo.currentIndexChanged.connect(lambda: self.switch_language(self.lang_combo.currentData()))
        self.lang_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {BRAND_PRIMARY};
                border-radius: 4px;
                padding: 3px 8px;
                font-size: 11px;
                min-width: 80px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        lang_layout.addWidget(self.lang_combo)
        header_layout.addWidget(lang_widget)
        
        # Version
        version = QLabel("v1.1.0")
        version.setStyleSheet("color: #999; font-size: 11px; margin-left: 10px;")
        header_layout.addWidget(version)
        
        layout.addWidget(header_widget)
    
    def create_status_section(self, layout):
        """Create status display"""
        status_widget = QWidget()
        status_widget.setObjectName("statusWidget")
        status_layout = QHBoxLayout(status_widget)
        
        # Status indicator
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet(f"color: {BRAND_DANGER}; font-size: 24px;")
        status_layout.addWidget(self.status_indicator)
        
        # Status text
        self.status_label = QLabel(self.tr('not_connected'))
        self.status_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        # Last sync time
        self.last_sync_label = QLabel(self.tr('last_sync_never'))
        self.last_sync_label.setStyleSheet("color: #666; font-size: 12px;")
        status_layout.addWidget(self.last_sync_label)
        
        layout.addWidget(status_widget)
    
    def create_license_section(self, layout):
        """Create license input section"""
        self.license_group = QGroupBox(self.tr('license_configuration'))
        license_layout = QVBoxLayout()
        
        # License key input
        key_layout = QHBoxLayout()
        self.license_label = QLabel(self.tr('license_key') + ":")
        key_layout.addWidget(self.license_label)
        
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText(self.tr('license_placeholder'))
        self.license_input.setText(self.settings.get('license_key', ''))
        key_layout.addWidget(self.license_input)
        
        self.connect_btn = QPushButton(self.tr('connect'))
        self.connect_btn.setObjectName("primaryButton")
        self.connect_btn.clicked.connect(self.connect_license)
        key_layout.addWidget(self.connect_btn)
        
        license_layout.addLayout(key_layout)
        
        # Company info (hidden initially)
        self.company_info_widget = QWidget()
        company_info_layout = QVBoxLayout(self.company_info_widget)
        company_info_layout.setContentsMargins(0, 10, 0, 0)
        
        self.company_name_label = QLabel()
        self.company_plan_label = QLabel()
        self.company_expiry_label = QLabel()
        
        company_info_layout.addWidget(self.company_name_label)
        company_info_layout.addWidget(self.company_plan_label)
        company_info_layout.addWidget(self.company_expiry_label)
        
        self.company_info_widget.setVisible(False)
        license_layout.addWidget(self.company_info_widget)
        
        self.license_group.setLayout(license_layout)
        layout.addWidget(self.license_group)
    
    def create_devices_section(self, layout):
        """Create devices list section"""
        self.devices_group = QGroupBox(self.tr('devices_cloud'))
        devices_layout = QVBoxLayout()
        
        # Devices list
        self.devices_list = QListWidget()
        self.devices_list.setMinimumHeight(150)
        devices_layout.addWidget(self.devices_list)
        
        # Device buttons
        device_buttons = QHBoxLayout()
        
        self.refresh_devices_btn = QPushButton(self.tr('refresh_from_cloud'))
        self.refresh_devices_btn.clicked.connect(self.load_company_devices)
        self.refresh_devices_btn.setEnabled(False)
        device_buttons.addWidget(self.refresh_devices_btn)
        
        device_buttons.addStretch()
        
        devices_layout.addLayout(device_buttons)
        
        self.devices_group.setLayout(devices_layout)
        layout.addWidget(self.devices_group)
    
    def create_control_buttons(self, layout):
        """Create sync control buttons"""
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        
        # Dashboard button
        self.dashboard_btn = QPushButton(self.tr('open_dashboard'))
        self.dashboard_btn.setObjectName("primaryButton")
        self.dashboard_btn.clicked.connect(self.open_dashboard)
        control_layout.addWidget(self.dashboard_btn)
        
        self.sync_now_btn = QPushButton(self.tr('sync_now'))
        self.sync_now_btn.setObjectName("successButton")
        self.sync_now_btn.clicked.connect(self.start_sync)
        self.sync_now_btn.setEnabled(False)
        control_layout.addWidget(self.sync_now_btn)
        
        self.start_sync_btn = QPushButton(self.tr('start_auto_sync'))
        self.start_sync_btn.setObjectName("primaryButton")
        self.start_sync_btn.clicked.connect(self.toggle_auto_sync)
        self.start_sync_btn.setEnabled(False)
        control_layout.addWidget(self.start_sync_btn)
        
        control_layout.addStretch()
        
        layout.addWidget(control_widget)
    
    def create_settings_section(self, layout):
        """Create settings section"""
        self.settings_group = QGroupBox(self.tr('settings'))
        settings_layout = QHBoxLayout()
        
        self.sync_interval_label = QLabel(self.tr('sync_interval') + ":")
        settings_layout.addWidget(self.sync_interval_label)
        
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setMinimum(5)
        self.interval_spinbox.setMaximum(120)
        self.interval_spinbox.setValue(self.settings.get('sync_interval', 15))
        self.interval_spinbox.setSuffix(" " + self.tr('minutes'))
        self.interval_spinbox.valueChanged.connect(self.save_settings)
        settings_layout.addWidget(self.interval_spinbox)
        
        self.startup_checkbox = QCheckBox(self.tr('startup'))
        self.startup_checkbox.setChecked(self.settings.get('auto_start', True))
        self.startup_checkbox.stateChanged.connect(self.save_settings)
        settings_layout.addWidget(self.startup_checkbox)
        
        self.notifications_checkbox = QCheckBox(self.tr('notifications'))
        self.notifications_checkbox.setChecked(self.settings.get('show_notifications', True))
        self.notifications_checkbox.stateChanged.connect(self.save_settings)
        settings_layout.addWidget(self.notifications_checkbox)
        
        settings_layout.addStretch()
        
        self.settings_group.setLayout(settings_layout)
        layout.addWidget(self.settings_group)
    
    def create_logs_section(self, layout):
        """Create logs display"""
        self.logs_group = QGroupBox(self.tr('activity_logs'))
        logs_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        logs_layout.addWidget(self.log_text)
        
        # Clear logs button
        self.clear_logs_btn = QPushButton(self.tr('clear_logs'))
        self.clear_logs_btn.clicked.connect(self.log_text.clear)
        logs_layout.addWidget(self.clear_logs_btn)
        
        self.logs_group.setLayout(logs_layout)
        layout.addWidget(self.logs_group)
    
    def create_system_tray(self):
        """Create system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # Tray menu
        tray_menu = QMenu()
        
        show_action = QAction(self.tr('show'), self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        dashboard_action = QAction(self.tr('open_dashboard'), self)
        dashboard_action.triggered.connect(self.open_dashboard)
        tray_menu.addAction(dashboard_action)
        
        tray_menu.addSeparator()
        
        sync_action = QAction(self.tr('sync_now'), self)
        sync_action.triggered.connect(self.start_sync)
        tray_menu.addAction(sync_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction(self.tr('quit'), self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.tray_activated)
    
    def load_logo_async(self):
        """Download and display logo asynchronously (non-blocking)"""
        class LogoDownloader(QThread):
            logo_ready = pyqtSignal(bytes)
            
            def run(self):
                try:
                    response = requests.get(LOGO_URL, timeout=5)
                    if response.status_code == 200:
                        self.logo_ready.emit(response.content)
                except:
                    pass
        
        def on_logo_ready(logo_data):
            try:
                pixmap = QPixmap()
                pixmap.loadFromData(logo_data)
                self.logo_label.setPixmap(pixmap)
                
                # Set tray icon and window icon
                icon = QIcon(pixmap)
                self.tray_icon.setIcon(icon)
                self.setWindowIcon(icon)
                
                # Save logo for future use
                icon_dir = os.path.join(os.path.expanduser("~"), ".attendux_sync")
                os.makedirs(icon_dir, exist_ok=True)
                icon_path = os.path.join(icon_dir, "logo.png")
                pixmap.save(icon_path, 'PNG')
            except Exception as e:
                print(f"Failed to set logo: {e}")
        
        # Try to load cached logo first (instant)
        try:
            icon_dir = os.path.join(os.path.expanduser("~"), ".attendux_sync")
            icon_path = os.path.join(icon_dir, "logo.png")
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path)
                self.logo_label.setPixmap(pixmap)
                icon = QIcon(pixmap)
                self.tray_icon.setIcon(icon)
                self.setWindowIcon(icon)
                return  # Use cached logo, no need to download
        except:
            pass
        
        # Download in background thread
        self.logo_downloader = LogoDownloader()
        self.logo_downloader.logo_ready.connect(on_logo_ready)
        self.logo_downloader.start()
    
    def auto_connect(self):
        """Auto-connect on startup"""
        self.connect_license()
        
        # If auto-sync was running before, resume it
        if self.settings.get('auto_sync_was_running', False) and self.api:
            QTimer.singleShot(2000, self.resume_auto_sync)
    
    def connect_license(self):
        """Connect to Attendux cloud (async to avoid UI freeze)"""
        license_key = self.license_input.text().strip()
        
        if not license_key:
            self.log("Please enter a license key", "error")
            return
        
        self.log("🔑 Verifying license...", "info")
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting..." if self.current_language == 'en' else "جاري الاتصال...")
        
        # Create API instance
        self.api = AttenduxAPI(license_key)
        
        # Verify license in background thread
        class LicenseVerifier(QThread):
            result_ready = pyqtSignal(dict)
            
            def __init__(self, api):
                super().__init__()
                self.api = api
            
            def run(self):
                try:
                    result = self.api.verify_license()
                    self.result_ready.emit(result if result else {})
                except Exception as e:
                    print(f"License verification error: {e}")
                    self.result_ready.emit({})
        
        def on_result_ready(result):
            if result and result.get('valid'):
                self.company_info = result.get('company', {})
                
                # Update UI
                self.status_indicator.setStyleSheet(f"color: {BRAND_SUCCESS}; font-size: 24px;")
                self.status_label.setText(f"✅ {self.tr('connected')} - {self.company_info.get('name', 'Unknown')}")
                
                # Show company info
                self.company_name_label.setText(f"{self.tr('company_label')}: {self.company_info.get('name', 'N/A')}")
                self.company_plan_label.setText(f"{self.tr('plan_label')}: {self.company_info.get('plan', 'N/A')}")
                
                expiry = self.company_info.get('license_expiry', 'N/A')
                self.company_expiry_label.setText(f"{self.tr('license_expires')}: {expiry}")
                self.company_info_widget.setVisible(True)
                
                # Enable controls
                self.refresh_devices_btn.setEnabled(True)
                self.sync_now_btn.setEnabled(True)
                self.start_sync_btn.setEnabled(True)
                
                # Save license key
                self.settings['license_key'] = license_key
                self.save_settings()
                
                self.log(f"✅ Connected as {self.company_info.get('name')}", "success")
                
                # Load devices (also async)
                QTimer.singleShot(500, self.load_company_devices)
                
            else:
                self.status_indicator.setStyleSheet(f"color: {BRAND_DANGER}; font-size: 24px;")
                self.status_label.setText("❌ Invalid License")
                self.log("❌ Invalid license key or expired", "error")
            
            self.connect_btn.setEnabled(True)
            self.connect_btn.setText(self.tr('connect'))
        
        self.license_verifier = LicenseVerifier(self.api)
        self.license_verifier.result_ready.connect(on_result_ready)
        self.license_verifier.start()
    
    def open_dashboard(self):
        """Open Attendux dashboard in embedded browser - fullscreen without toolbar"""
        dashboard_url = "https://app.attendux.com"
        
        # If QtWebEngine is not available, use external browser
        if not WEBENGINE_AVAILABLE:
            import webbrowser
            webbrowser.open(dashboard_url)
            self.log(f"🌐 Opening dashboard in external browser", "info")
            return
        
        try:
            # Create dashboard window if not exists
            if not self.dashboard_browser or not self.dashboard_browser.isVisible():
                self.dashboard_browser = QWidget()
                self.dashboard_browser.setWindowTitle("أتندوكس - لوحة التحكم")
                
                # Make it fullscreen or maximized
                screen = QApplication.desktop().screenGeometry()
                self.dashboard_browser.setGeometry(0, 0, screen.width(), screen.height())
                self.dashboard_browser.showMaximized()  # Start maximized
                
                # Create layout with no margins for fullscreen
                browser_layout = QVBoxLayout(self.dashboard_browser)
                browser_layout.setContentsMargins(0, 0, 0, 0)
                browser_layout.setSpacing(0)
                
                try:
                    # Configure persistent session profile for cookie/session storage
                    if WEBENGINE_AVAILABLE:
                        from PyQt5.QtWebEngineWidgets import QWebEngineProfile
                        
                        # Get or create persistent profile
                        profile = QWebEngineProfile.defaultProfile()
                        
                        # Enable persistent cookies (critical for login sessions)
                        profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
                        
                        # Set cache directory for persistence
                        import os
                        cache_dir = os.path.expanduser("~/.attendux_sync/cache")
                        storage_dir = os.path.expanduser("~/.attendux_sync/storage")
                        
                        try:
                            os.makedirs(cache_dir, exist_ok=True)
                            os.makedirs(storage_dir, exist_ok=True)
                        except:
                            pass
                        
                        profile.setCachePath(cache_dir)
                        profile.setPersistentStoragePath(storage_dir)
                        
                        # Set a proper User-Agent to avoid detection issues
                        profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                        
                        # Disable HTTP strict transport security (HSTS) to avoid issues
                        profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
                    
                    # Create web view - takes full window (no toolbar)
                    web_view = QWebEngineView()
                    
                    # Track URL changes to detect redirect loops
                    self.url_change_count = 0
                    self.last_url = None
                    
                    # Add URL change handler to detect refresh issues
                    def on_url_changed(url):
                        url_str = url.toString()
                        self.log(f"🌐 URL Changed: {url_str}", "info")
                        
                        # Detect redirect loop (same URL changing repeatedly)
                        if self.last_url == url_str:
                            self.url_change_count += 1
                            if self.url_change_count > 3:
                                self.log(f"⚠️ WARNING: Redirect loop detected! URL: {url_str}", "error")
                                self.log(f"⚠️ Stopping page load to prevent infinite loop", "error")
                                web_view.stop()
                                return
                        else:
                            self.url_change_count = 0
                            self.last_url = url_str
                    
                    def on_load_started():
                        self.log(f"🔄 Page load started...", "info")
                    
                    def on_load_finished(success):
                        if success:
                            self.log(f"✅ Page loaded successfully", "info")
                            # Inject JavaScript to disable any auto-refresh or meta refresh tags
                            inject_script = """
                            (function() {
                                // Remove any meta refresh tags
                                var metaRefresh = document.querySelector('meta[http-equiv="refresh"]');
                                if (metaRefresh) {
                                    metaRefresh.remove();
                                    console.log('Attendux Sync: Removed meta refresh tag');
                                }
                                
                                // Store original reload function
                                var originalReload = window.location.reload;
                                var reloadAttempts = 0;
                                
                                // Override location.reload to prevent auto-refresh
                                window.location.reload = function(forcedReload) {
                                    reloadAttempts++;
                                    console.warn('Attendux Sync: Blocked automatic page reload attempt #' + reloadAttempts);
                                    console.trace('Reload called from:');
                                    // Don't actually reload
                                    return false;
                                };
                                
                                // Prevent setInterval/setTimeout from calling reload
                                var originalSetInterval = window.setInterval;
                                window.setInterval = function(func, delay) {
                                    // Check if function calls reload
                                    var funcStr = func.toString();
                                    if (funcStr.includes('reload') || funcStr.includes('location.href')) {
                                        console.warn('Attendux Sync: Blocked setInterval that calls reload/redirect');
                                        return 0; // Return dummy interval ID
                                    }
                                    return originalSetInterval.apply(this, arguments);
                                };
                                
                                console.log('Attendux Sync: Auto-refresh prevention initialized');
                            })();
                            """
                            web_view.page().runJavaScript(inject_script)
                        else:
                            self.log(f"❌ Page load failed", "error")
                    
                    web_view.urlChanged.connect(on_url_changed)
                    web_view.loadStarted.connect(on_load_started)
                    web_view.loadFinished.connect(on_load_finished)
                    
                    # Enable web features that might be needed
                    if WEBENGINE_AVAILABLE:
                        from PyQt5.QtWebEngineWidgets import QWebEngineSettings
                        settings = web_view.settings()
                        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
                        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
                        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
                        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
                        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
                        
                        # BALANCED: Disable heavy features to reduce lag
                        settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)  # Disable WebGL (causes lag)
                        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, False)  # Disable 2D accel (causes lag)
                        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, False)  # Skip favicons (faster load)
                        
                        # Additional optimization settings
                        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)  # No plugins needed
                        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, False)  # No smooth scroll
                        settings.setAttribute(QWebEngineSettings.FocusOnNavigationEnabled, False)  # Reduce focus events
                        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, False)  # Security + speed
                        
                        self.log(f"✅ WebEngine: Balanced mode (WebGL OFF, 2D Canvas OFF, optimized)", "info")
                    
                    # BALANCED: Optimize rendering for stability and performance
                    web_view.setUpdatesEnabled(True)
                    web_view.setAttribute(Qt.WA_OpaquePaintEvent, True)  # Opaque (faster, no transparency)
                    web_view.setAttribute(Qt.WA_NoSystemBackground, True)  # Skip system bg (faster)
                    web_view.setAttribute(Qt.WA_DontCreateNativeAncestors, True)  # Reduce native widget overhead
                    
                    # Limit render updates (reduces CPU usage)
                    if PLATFORM == 'Windows':
                        web_view.setUpdatesEnabled(True)  # Keep updates but optimize
                    
                    self.log(f"✅ Rendering: Balanced mode (opaque paint, optimized updates)", "info")
                    
                    web_view.setUrl(QUrl(dashboard_url))
                    browser_layout.addWidget(web_view)
                    
                    # Store web_view reference for potential future use
                    self.dashboard_webview = web_view
                except Exception as web_error:
                    # Fallback: Open in external browser if QtWebEngine fails
                    import webbrowser
                    webbrowser.open(dashboard_url)
                    self.dashboard_browser.close()
                    self.log(f"🌐 Opening dashboard in external browser (QtWebEngine error)", "info")
                    return
            
            # Show the browser window
            self.dashboard_browser.show()
            self.dashboard_browser.raise_()
            self.dashboard_browser.activateWindow()
            
            self.log(f"🌐 {self.tr('open_dashboard')}: {dashboard_url}", "info")
            
            if self.notifications_checkbox.isChecked():
                msg_title = "لوحة التحكم" if self.current_language == 'ar' else "Dashboard Opened"
                msg_text = "تم فتح لوحة التحكم" if self.current_language == 'ar' else "Attendux dashboard opened"
                self.tray_icon.showMessage(
                    msg_title,
                    msg_text,
                    QSystemTrayIcon.Information,
                    2000
                )
        except Exception as e:
            self.log(f"❌ Failed to open dashboard: {str(e)}", "error")
    
    def load_company_devices(self):
        """Load devices from cloud for this company (async)"""
        if not self.api:
            return
        
        self.log("📡 Loading devices from cloud...", "info")
        self.refresh_devices_btn.setEnabled(False)
        
        class DeviceLoader(QThread):
            devices_ready = pyqtSignal(list)
            
            def __init__(self, api):
                super().__init__()
                self.api = api
            
            def run(self):
                try:
                    devices = self.api.get_company_devices()
                    self.devices_ready.emit(devices if devices else [])
                except Exception as e:
                    print(f"Device loading error: {e}")
                    self.devices_ready.emit([])
        
        def on_devices_ready(devices):
            if devices:
                self.settings['devices'] = devices
                self.save_settings()
                
                # Update device list
                self.devices_list.clear()
                for device in devices:
                    item_text = f"✓ {device['name']} - {device['ip']}:{device['port']} (ID: {device.get('id', 'N/A')})"
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.UserRole, device)
                    self.devices_list.addItem(item)
                
                self.log(f"✅ Loaded {len(devices)} devices for your company", "success")
            else:
                self.log("ℹ️ No devices found. Add devices in Attendux dashboard first.", "warning")
            
            self.refresh_devices_btn.setEnabled(True)
        
        self.device_loader = DeviceLoader(self.api)
        self.device_loader.devices_ready.connect(on_devices_ready)
        self.device_loader.start()
    
    def start_sync(self):
        """Start sync process"""
        if self.sync_worker and self.sync_worker.isRunning():
            self.log("⚠️ Sync already in progress", "warning")
            return
        
        devices = self.settings.get('devices', [])
        
        if not devices:
            self.log("❌ No devices to sync. Load devices first.", "error")
            return
        
        # Disable buttons
        self.sync_now_btn.setEnabled(False)
        
        # Start worker
        self.sync_worker = SyncWorker(self.api, devices)
        self.sync_worker.log_signal.connect(self.log)
        self.sync_worker.sync_complete_signal.connect(self.sync_completed)
        self.sync_worker.start()
    
    def sync_completed(self, result):
        """Handle sync completion"""
        # Update last sync time
        self.settings['last_sync'] = result['timestamp']
        self.save_settings()
        
        self.last_sync_label.setText(f"{self.tr('last_sync')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Re-enable buttons
        self.sync_now_btn.setEnabled(True)
        
        # Show notification
        if self.notifications_checkbox.isChecked():
            if len(result['errors']) == 0:
                self.tray_icon.showMessage(
                    "Sync Complete",
                    f"Successfully synced {result['total_synced']} records from {result['devices_count']} devices",
                    QSystemTrayIcon.Information,
                    3000
                )
            else:
                self.tray_icon.showMessage(
                    "Sync Completed with Errors",
                    f"Synced {result['total_synced']} records, but {len(result['errors'])} errors occurred",
                    QSystemTrayIcon.Warning,
                    3000
                )
    
    def toggle_auto_sync(self):
        """Toggle auto-sync on/off"""
        if self.sync_timer.isActive():
            # Stop auto-sync
            self.sync_timer.stop()
            self.start_sync_btn.setText(self.tr('start_auto_sync'))
            self.start_sync_btn.setObjectName("primaryButton")
            self.log("⏸ Auto-sync stopped", "info")
            
            # Save state
            self.settings['auto_sync_was_running'] = False
            SettingsManager.save(self.settings)
        else:
            # Start auto-sync
            interval = self.interval_spinbox.value() * 60 * 1000  # Convert to milliseconds
            self.sync_timer.start(interval)
            self.start_sync_btn.setText(self.tr('stop_auto_sync'))
            self.start_sync_btn.setObjectName("dangerButton")
            self.log(f"▶ Auto-sync started (every {self.interval_spinbox.value()} minutes)", "success")
            
            # Save state
            self.settings['auto_sync_was_running'] = True
            SettingsManager.save(self.settings)
            
            # Do immediate sync
            self.start_sync()
        
        # Refresh button style
        self.start_sync_btn.setStyle(self.start_sync_btn.style())
    
    def resume_auto_sync(self):
        """Resume auto-sync after app restart"""
        if not self.sync_timer.isActive() and self.settings.get('auto_sync_was_running', False):
            self.log("🔄 Resuming auto-sync from previous session...", "info")
            self.toggle_auto_sync()
    
    def save_settings(self):
        """Save settings to file"""
        self.settings['sync_interval'] = self.interval_spinbox.value()
        
        # Handle startup (Windows or macOS)
        auto_start_enabled = self.startup_checkbox.isChecked()
        if auto_start_enabled != self.settings.get('auto_start'):
            if auto_start_enabled:
                self.add_to_startup()
            else:
                self.remove_from_startup()
        
        self.settings['auto_start'] = auto_start_enabled
        self.settings['show_notifications'] = self.notifications_checkbox.isChecked()
        SettingsManager.save(self.settings)
    
    def add_to_startup(self):
        """Add application to system startup (Windows or macOS)"""
        if PLATFORM == 'Windows':
            self.add_to_windows_startup()
        elif PLATFORM == 'Darwin':
            self.add_to_macos_startup()
        else:
            self.log("⚠️ Auto-startup not supported on this platform", "warning")
    
    def remove_from_startup(self):
        """Remove application from system startup"""
        if PLATFORM == 'Windows':
            self.remove_from_windows_startup()
        elif PLATFORM == 'Darwin':
            self.remove_from_macos_startup()
    
    def add_to_windows_startup(self):
        """Add application to Windows startup"""
        if not WINDOWS_STARTUP_AVAILABLE:
            return
        
        try:
            # Get executable path
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable
            else:
                exe_path = os.path.abspath(__file__)
            
            # Open Windows startup registry key
            key = reg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            # Add entry
            reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(reg_key, "AttenduxSyncAgent", 0, reg.REG_SZ, exe_path)
            reg.CloseKey(reg_key)
            
            self.log("✅ Added to Windows startup", "success")
        except Exception as e:
            self.log(f"❌ Failed to add to startup: {str(e)}", "error")
    
    def remove_from_windows_startup(self):
        """Remove application from Windows startup"""
        if not WINDOWS_STARTUP_AVAILABLE:
            return
        
        try:
            key = reg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            reg_key = reg.OpenKey(key, key_path, 0, reg.KEY_SET_VALUE)
            try:
                reg.DeleteValue(reg_key, "AttenduxSyncAgent")
                self.log("✅ Removed from Windows startup", "success")
            except FileNotFoundError:
                pass
            reg.CloseKey(reg_key)
        except Exception as e:
            self.log(f"❌ Failed to remove from startup: {str(e)}", "error")
    
    def add_to_macos_startup(self):
        """Add application to macOS login items"""
        if not MACOS_STARTUP_AVAILABLE:
            return
        
        try:
            # Get app path
            if getattr(sys, 'frozen', False):
                # Running as .app bundle
                app_path = sys.executable
                # Go up to .app bundle
                while not app_path.endswith('.app'):
                    app_path = os.path.dirname(app_path)
                    if app_path == '/' or app_path == '':
                        app_path = sys.executable
                        break
            else:
                app_path = os.path.abspath(__file__)
            
            # Create LaunchAgent plist
            plist_dir = os.path.expanduser('~/Library/LaunchAgents')
            os.makedirs(plist_dir, exist_ok=True)
            
            plist_path = os.path.join(plist_dir, 'com.attendux.syncagent.plist')
            
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.attendux.syncagent</string>
    <key>ProgramArguments</key>
    <array>
        <string>open</string>
        <string>{app_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>"""
            
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            self.log("✅ Added to macOS login items", "success")
        except Exception as e:
            self.log(f"❌ Failed to add to login items: {str(e)}", "error")
    
    def remove_from_macos_startup(self):
        """Remove application from macOS login items"""
        if not MACOS_STARTUP_AVAILABLE:
            return
        
        try:
            plist_path = os.path.expanduser('~/Library/LaunchAgents/com.attendux.syncagent.plist')
            if os.path.exists(plist_path):
                os.remove(plist_path)
                self.log("✅ Removed from macOS login items", "success")
        except Exception as e:
            self.log(f"❌ Failed to remove from login items: {str(e)}", "error")
    
    def log(self, message, level="info"):
        """Add log message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Color based on level
        if level == "success":
            color = BRAND_SUCCESS
        elif level == "error":
            color = BRAND_DANGER
        elif level == "warning":
            color = BRAND_WARNING
        else:
            color = BRAND_GRAY_800
        
        html = f'<span style="color: {color};">[{timestamp}] {message}</span>'
        self.log_text.append(html)
        
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()  # Show in normal state (not maximized)
                self.raise_()  # Bring to front
                self.activateWindow()  # Give focus
    
    def closeEvent(self, event):
        """Handle window close"""
        event.ignore()
        self.hide()
        
        if self.notifications_checkbox.isChecked():
            self.tray_icon.showMessage(
                "Attendux Sync Agent",
                "Application minimized to system tray",
                QSystemTrayIcon.Information,
                2000
            )
    
    def quit_app(self):
        """Quit application"""
        # Stop sync if running
        if self.sync_worker and self.sync_worker.isRunning():
            self.sync_worker.stop()
            self.sync_worker.wait()
        
        # Stop timer
        self.sync_timer.stop()
        
        # Quit
        QApplication.quit()
    
    def get_stylesheet(self):
        """Get application stylesheet with proper sizing"""
        return f"""
            * {{
                font-family: 'Segoe UI', sans-serif;
            }}
            
            QMainWindow {{
                background-color: {BRAND_GRAY_100};
            }}
            
            QGroupBox {{
                font-weight: bold;
                font-size: 13px;
                border: 2px solid {BRAND_PRIMARY};
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                padding-bottom: 10px;
                background-color: white;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
                color: {BRAND_PRIMARY_DARK};
            }}
            
            #statusWidget {{
                background: white;
                border-radius: 8px;
                padding: 15px;
                min-height: 40px;
            }}
            
            QPushButton {{
                background-color: {BRAND_PRIMARY};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
                min-width: 120px;
                min-height: 42px;
            }}
            
            QPushButton:hover {{
                background-color: {BRAND_PRIMARY_DARK};
                transform: scale(1.02);
            }}
            
            QPushButton:pressed {{
                background-color: {BRAND_PRIMARY_DARK};
                padding-top: 14px;
            }}
            
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
            
            QPushButton#primaryButton {{
                background-color: {BRAND_PRIMARY};
            }}
            
            QPushButton#primaryButton:hover {{
                background-color: {BRAND_PRIMARY_DARK};
            }}
            
            QPushButton#successButton {{
                background-color: {BRAND_SUCCESS};
            }}
            
            QPushButton#successButton:hover {{
                background-color: #059669;
            }}
            
            QPushButton#dangerButton {{
                background-color: {BRAND_DANGER};
            }}
            
            QPushButton#dangerButton:hover {{
                background-color: #dc2626;
            }}
            
            QLineEdit {{
                padding: 12px 16px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background: white;
                font-size: 13px;
                min-height: 42px;
            }}
            
            QLineEdit:focus {{
                border-color: {BRAND_PRIMARY};
                border-width: 2px;
            }}
            
            QListWidget {{
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background: white;
                padding: 8px;
                font-size: 13px;
            }}
            
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid #f3f4f6;
                min-height: 36px;
            }}
            
            QListWidget::item:hover {{
                background-color: #f0f9ff;
                border-radius: 4px;
            }}
            
            QTextEdit {{
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background: #fafafa;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.5;
            }}
            
            QSpinBox {{
                padding: 10px 12px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background: white;
                font-size: 13px;
                min-height: 42px;
            }}
            
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 24px;
                border-radius: 4px;
            }}
            
            QCheckBox {{
                spacing: 8px;
                font-size: 13px;
                padding: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid #e5e7eb;
                border-radius: 5px;
                background: white;
            }}
            
            QCheckBox::indicator:hover {{
                border-color: {BRAND_PRIMARY};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {BRAND_PRIMARY};
                border-color: {BRAND_PRIMARY};
            }}
            
            QComboBox {{
                padding: 10px 12px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                background: white;
                font-size: 13px;
                min-height: 42px;
            }}
            
            QComboBox:hover {{
                border-color: {BRAND_PRIMARY};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border: solid {BRAND_PRIMARY};
                border-width: 0 2px 2px 0;
                padding: 3px;
                transform: rotate(45deg);
            }}
            
            QLabel {{
                font-size: 13px;
            }}
        """


def main():
    """Main entry point"""
    try:
        # Windows-specific fixes
        if PLATFORM == 'Windows':
            # BALANCED: Moderate acceleration (no flash, good performance)
            # Use WARP (software renderer) instead of full hardware for stability
            os.environ['QT_ANGLE_PLATFORM'] = 'warp'  # Software D3D renderer (stable, no flash)
            
            # Chromium flags for BALANCED performance
            os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu-vsync --disable-smooth-scrolling --enable-low-end-device-mode --disable-accelerated-video-decode'
            os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
            
            # Moderate OpenGL - not full hardware, not full software
            os.environ['QT_OPENGL'] = 'angle'  # Use ANGLE for compatibility
            
            # Limit browser processes to reduce memory/CPU usage
            os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] += ' --single-process --disable-extensions'
            
            print("✅ Windows: Balanced mode (WARP renderer + ANGLE + low-end optimizations)")
            
            # Fix for Windows 10/11 high DPI scaling
            try:
                from PyQt5.QtCore import Qt
                # Disable high DPI scaling to prevent rendering issues
                # (will be overridden by AA_DisableHighDpiScaling in app creation)
                # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
                # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
            except:
                pass
            
            # Fix for Windows console window appearing
            try:
                import ctypes
                # Set App User Model ID to group windows under single taskbar icon
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Attendux.SyncAgent.1.0')
                
                # Hide the main window from taskbar (only show tray icon)
                # This prevents duplicate icons in Windows taskbar
                import ctypes.wintypes
                GWL_EXSTYLE = -20
                WS_EX_TOOLWINDOW = 0x00000080
                WS_EX_APPWINDOW = 0x00040000
            except:
                pass
            
            # Set Windows process priority to normal to avoid freezing
            try:
                import psutil
                p = psutil.Process()
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
            except:
                pass
        
        app = QApplication(sys.argv)
        app.setApplicationName("Attendux Sync Agent")
        app.setOrganizationName("Attendux")
        
        # BALANCED: Windows-specific settings for stability + performance
        if PLATFORM == 'Windows':
            # Use ANGLE (compatible with more systems) instead of Desktop OpenGL
            # This prevents sluggishness on some GPU configurations
            # Note: NOT using AA_UseSoftwareOpenGL or AA_UseDesktopOpenGL
            # Let Qt auto-detect the best renderer
            
            # Disable high DPI scaling to reduce rendering overhead
            app.setAttribute(Qt.AA_DisableHighDpiScaling, True)
            
            # Share OpenGL contexts for better memory usage
            app.setAttribute(Qt.AA_ShareOpenGLContexts, True)
            
            # Use raster engine for widgets (faster than native)
            app.setAttribute(Qt.AA_UseHighDpiPixmaps, False)
            
            print("✅ Windows: Balanced mode (Auto-detect renderer + DPI optimizations)")
        
        # Set default font for better Windows rendering
        if PLATFORM == 'Windows':
            from PyQt5.QtGui import QFont
            font = QFont("Segoe UI", 9)
            app.setFont(font)
        
        # Process events before showing window to ensure UI is responsive
        QApplication.processEvents()
        
        window = AttenduxSyncAgent()
        
        # Process events again to finish initialization
        QApplication.processEvents()
        
        # On Windows, start minimized to tray to avoid duplicate taskbar icons
        # User can open window from tray menu
        if PLATFORM == 'Windows':
            # Don't call window.show() - start in tray only
            window.hide()
            # Show notification that app started in tray
            if window.tray_icon:
                window.tray_icon.showMessage(
                    "Attendux Sync Agent",
                    "Application started in system tray. Double-click tray icon to open.",
                    QSystemTrayIcon.Information,
                    3000
                )
        else:
            # On Mac/Linux, show window normally
            window.show()
        
        # Final event processing to ensure UI is ready
        QApplication.processEvents()
        
        sys.exit(app.exec_())
        
    except Exception as e:
        # Show error dialog on crash
        import traceback
        error_details = traceback.format_exc()
        
        try:
            from PyQt5.QtWidgets import QMessageBox
            error_app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Attendux Sync Agent - Startup Error")
            msg.setText("Application failed to start")
            msg.setInformativeText(str(e))
            msg.setDetailedText(f"Platform: {PLATFORM}\nPython: {sys.version}\n\nFull Error:\n{error_details}")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except:
            print(f"Fatal error: {e}")
            print(error_details)
        sys.exit(1)


if __name__ == '__main__':
    main()
