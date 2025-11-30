#!/usr/bin/env python3
"""
Download Attendux logo for app icon
"""

import requests
import sys

LOGO_URL = "https://app.attendux.com/public/storage/logo.png"
OUTPUT_FILE = "logo.png"

def download_logo():
    """Download logo from server"""
    try:
        print(f"Downloading logo from {LOGO_URL}...")
        response = requests.get(LOGO_URL, timeout=10)
        
        if response.status_code == 200:
            with open(OUTPUT_FILE, 'wb') as f:
                f.write(response.content)
            print(f"✅ Logo saved to {OUTPUT_FILE}")
            return True
        else:
            print(f"❌ Failed to download logo: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading logo: {e}")
        return False

if __name__ == '__main__':
    success = download_logo()
    sys.exit(0 if success else 1)
