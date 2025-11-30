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
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

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
            'last_sync': None
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
        self.api = None
        self.company_info = None
        self.sync_worker = None
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.start_sync)
        
        self.init_ui()
        self.load_logo()
        
        # Auto-connect if license key exists
        if self.settings.get('license_key'):
            QTimer.singleShot(1000, self.auto_connect)
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle('Attendux Sync Agent')
        self.setMinimumSize(900, 700)
        self.setStyleSheet(self.get_stylesheet())
        
        # Center window
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(
            (screen.width() - 900) // 2,
            (screen.height() - 700) // 2,
            900, 700
        )
        
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
        title = QLabel("Attendux Sync Agent")
        title.setObjectName("title")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: " + BRAND_PRIMARY_DARK)
        subtitle = QLabel("Multi-Tenant ZKTeco Device Synchronization")
        subtitle.setStyleSheet("font-size: 12px; color: #666;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        
        header_layout.addStretch()
        
        # Version
        version = QLabel("v1.0.0")
        version.setStyleSheet("color: #999; font-size: 11px;")
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
        self.status_label = QLabel("Not Connected")
        self.status_label.setStyleSheet("font-size: 16px; font-weight: 600;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        # Last sync time
        self.last_sync_label = QLabel("Last sync: Never")
        self.last_sync_label.setStyleSheet("color: #666; font-size: 12px;")
        status_layout.addWidget(self.last_sync_label)
        
        layout.addWidget(status_widget)
    
    def create_license_section(self, layout):
        """Create license input section"""
        license_group = QGroupBox("License Configuration")
        license_layout = QVBoxLayout()
        
        # License key input
        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("License Key:"))
        
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("ATX-XXXX-XXXX-XXXX-XXXX")
        self.license_input.setText(self.settings.get('license_key', ''))
        key_layout.addWidget(self.license_input)
        
        self.connect_btn = QPushButton("Connect")
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
        
        license_group.setLayout(license_layout)
        layout.addWidget(license_group)
    
    def create_devices_section(self, layout):
        """Create devices list section"""
        devices_group = QGroupBox("Devices (Loaded from Cloud)")
        devices_layout = QVBoxLayout()
        
        # Devices list
        self.devices_list = QListWidget()
        self.devices_list.setMinimumHeight(150)
        devices_layout.addWidget(self.devices_list)
        
        # Device buttons
        device_buttons = QHBoxLayout()
        
        self.refresh_devices_btn = QPushButton("↻ Refresh from Cloud")
        self.refresh_devices_btn.clicked.connect(self.load_company_devices)
        self.refresh_devices_btn.setEnabled(False)
        device_buttons.addWidget(self.refresh_devices_btn)
        
        device_buttons.addStretch()
        
        devices_layout.addLayout(device_buttons)
        
        devices_group.setLayout(devices_layout)
        layout.addWidget(devices_group)
    
    def create_control_buttons(self, layout):
        """Create sync control buttons"""
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        
        self.sync_now_btn = QPushButton("▶ Sync Now")
        self.sync_now_btn.setObjectName("successButton")
        self.sync_now_btn.clicked.connect(self.start_sync)
        self.sync_now_btn.setEnabled(False)
        control_layout.addWidget(self.sync_now_btn)
        
        self.auto_sync_btn = QPushButton("⏱ Start Auto-Sync")
        self.auto_sync_btn.setObjectName("primaryButton")
        self.auto_sync_btn.clicked.connect(self.toggle_auto_sync)
        self.auto_sync_btn.setEnabled(False)
        control_layout.addWidget(self.auto_sync_btn)
        
        control_layout.addStretch()
        
        layout.addWidget(control_widget)
    
    def create_settings_section(self, layout):
        """Create settings section"""
        settings_group = QGroupBox("Settings")
        settings_layout = QHBoxLayout()
        
        settings_layout.addWidget(QLabel("Sync Interval:"))
        
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setMinimum(5)
        self.interval_spinbox.setMaximum(120)
        self.interval_spinbox.setValue(self.settings.get('sync_interval', 15))
        self.interval_spinbox.setSuffix(" minutes")
        self.interval_spinbox.valueChanged.connect(self.save_settings)
        settings_layout.addWidget(self.interval_spinbox)
        
        self.auto_start_checkbox = QCheckBox("Start with Windows")
        self.auto_start_checkbox.setChecked(self.settings.get('auto_start', True))
        self.auto_start_checkbox.stateChanged.connect(self.save_settings)
        settings_layout.addWidget(self.auto_start_checkbox)
        
        self.notifications_checkbox = QCheckBox("Show Notifications")
        self.notifications_checkbox.setChecked(self.settings.get('show_notifications', True))
        self.notifications_checkbox.stateChanged.connect(self.save_settings)
        settings_layout.addWidget(self.notifications_checkbox)
        
        settings_layout.addStretch()
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
    
    def create_logs_section(self, layout):
        """Create logs display"""
        logs_group = QGroupBox("Activity Logs")
        logs_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        logs_layout.addWidget(self.log_text)
        
        # Clear logs button
        clear_logs_btn = QPushButton("Clear Logs")
        clear_logs_btn.clicked.connect(self.log_text.clear)
        logs_layout.addWidget(clear_logs_btn)
        
        logs_group.setLayout(logs_layout)
        layout.addWidget(logs_group)
    
    def create_system_tray(self):
        """Create system tray icon"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # Tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        sync_action = QAction("Sync Now", self)
        sync_action.triggered.connect(self.start_sync)
        tray_menu.addAction(sync_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.tray_activated)
    
    def load_logo(self):
        """Download and display logo"""
        try:
            response = requests.get(LOGO_URL, timeout=5)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.logo_label.setPixmap(pixmap)
                
                # Set tray icon
                icon = QIcon(pixmap)
                self.tray_icon.setIcon(icon)
                self.setWindowIcon(icon)
        except Exception as e:
            print(f"Failed to load logo: {e}")
    
    def auto_connect(self):
        """Auto-connect on startup"""
        self.connect_license()
    
    def connect_license(self):
        """Connect to Attendux cloud"""
        license_key = self.license_input.text().strip()
        
        if not license_key:
            self.log("Please enter a license key", "error")
            return
        
        self.log("🔑 Verifying license...", "info")
        self.connect_btn.setEnabled(False)
        
        # Create API instance
        self.api = AttenduxAPI(license_key)
        
        # Verify license
        result = self.api.verify_license()
        
        if result and result.get('valid'):
            self.company_info = result.get('company', {})
            
            # Update UI
            self.status_indicator.setStyleSheet(f"color: {BRAND_SUCCESS}; font-size: 24px;")
            self.status_label.setText(f"✅ Connected - {self.company_info.get('name', 'Unknown')}")
            
            # Show company info
            self.company_name_label.setText(f"Company: {self.company_info.get('name', 'N/A')}")
            self.company_plan_label.setText(f"Plan: {self.company_info.get('plan', 'N/A')}")
            
            expiry = self.company_info.get('license_expiry', 'N/A')
            self.company_expiry_label.setText(f"License Expires: {expiry}")
            self.company_info_widget.setVisible(True)
            
            # Enable controls
            self.refresh_devices_btn.setEnabled(True)
            self.sync_now_btn.setEnabled(True)
            self.auto_sync_btn.setEnabled(True)
            
            # Save license key
            self.settings['license_key'] = license_key
            self.save_settings()
            
            self.log(f"✅ Connected as {self.company_info.get('name')}", "success")
            
            # Load devices
            self.load_company_devices()
            
        else:
            self.status_indicator.setStyleSheet(f"color: {BRAND_DANGER}; font-size: 24px;")
            self.status_label.setText("❌ Invalid License")
            self.log("❌ Invalid license key or expired", "error")
        
        self.connect_btn.setEnabled(True)
    
    def load_company_devices(self):
        """Load devices from cloud for this company"""
        if not self.api:
            return
        
        self.log("📡 Loading devices from cloud...", "info")
        
        devices = self.api.get_company_devices()
        
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
        
        self.last_sync_label.setText(f"Last sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
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
            self.auto_sync_btn.setText("⏱ Start Auto-Sync")
            self.auto_sync_btn.setObjectName("primaryButton")
            self.log("⏸ Auto-sync stopped", "info")
        else:
            # Start auto-sync
            interval = self.interval_spinbox.value() * 60 * 1000  # Convert to milliseconds
            self.sync_timer.start(interval)
            self.auto_sync_btn.setText("⏹ Stop Auto-Sync")
            self.auto_sync_btn.setObjectName("dangerButton")
            self.log(f"▶ Auto-sync started (every {self.interval_spinbox.value()} minutes)", "success")
            
            # Do immediate sync
            self.start_sync()
        
        # Refresh button style
        self.auto_sync_btn.setStyle(self.auto_sync_btn.style())
    
    def save_settings(self):
        """Save settings to file"""
        self.settings['sync_interval'] = self.interval_spinbox.value()
        self.settings['auto_start'] = self.auto_start_checkbox.isChecked()
        self.settings['show_notifications'] = self.notifications_checkbox.isChecked()
        SettingsManager.save(self.settings)
    
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
                self.show()
                self.activateWindow()
    
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
        """Get application stylesheet"""
        return f"""
            QMainWindow {{
                background-color: {BRAND_GRAY_100};
            }}
            
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {BRAND_PRIMARY};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: {BRAND_PRIMARY_DARK};
            }}
            
            #statusWidget {{
                background: white;
                border-radius: 8px;
                padding: 10px;
            }}
            
            QPushButton {{
                background-color: {BRAND_PRIMARY};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                min-width: 100px;
            }}
            
            QPushButton:hover {{
                background-color: {BRAND_PRIMARY_DARK};
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
                padding: 8px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background: white;
            }}
            
            QLineEdit:focus {{
                border-color: {BRAND_PRIMARY};
            }}
            
            QListWidget {{
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background: white;
                padding: 5px;
            }}
            
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #f3f4f6;
            }}
            
            QListWidget::item:hover {{
                background-color: #f0f9ff;
            }}
            
            QTextEdit {{
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background: #fafafa;
                padding: 5px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
            }}
            
            QSpinBox {{
                padding: 6px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background: white;
            }}
            
            QCheckBox {{
                spacing: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid #e5e7eb;
                border-radius: 4px;
                background: white;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {BRAND_PRIMARY};
                border-color: {BRAND_PRIMARY};
            }}
        """


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Attendux Sync Agent")
    app.setOrganizationName("Attendux")
    
    window = AttenduxSyncAgent()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
