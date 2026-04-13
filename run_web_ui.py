#!/usr/bin/env python
"""
Quick launcher for Naukri Job Automation Web UI
Automatically opens browser and serves on localhost:5000
"""

import os
import sys
import time
import webbrowser
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("🚀 NAUKRI JOB AUTOMATION - WEB UI LAUNCHER")
print("="*70 + "\n")

# Check dependencies
print("✓ Checking dependencies...")
try:
    import flask
    print("  ✓ Flask installed")
except ImportError:
    print("  ✗ Flask not found. Run: pip install flask==2.3.3")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("  ✓ Environment variables loaded")
except ImportError:
    print("  ⚠ python-dotenv not found (optional)")

# Check credentials
email = os.getenv('NAUKRI_EMAIL')
password = os.getenv('NAUKRI_PASSWORD')

if not email or not password or email == 'set in .env file':
    print("\n⚠️  WARNING: Credentials not configured!")
    print("   Please add to .env file:")
    print("   NAUKRI_EMAIL=your-email@gmail.com")
    print("   NAUKRI_PASSWORD=your-password")
    print("\n   Web UI will still start but won't be able to search/apply.")
else:
    print(f"  ✓ Credentials configured ({email[:15]}...)")

# Create required directories
os.makedirs('data/logs', exist_ok=True)
os.makedirs('templates', exist_ok=True)
print("  ✓ Data directories verified")

print("\n" + "="*70)
print("🌐 STARTING WEB SERVER")
print("="*70 + "\n")

print("📍 Web UI will be available at: http://localhost:5000")
print("   Press Ctrl+C to stop the server\n")

# Import and run app
print("Loading application...")
try:
    from app import app, logger
    
    print("✓ Application loaded successfully\n")
    
    # Open browser after 2 seconds
    def open_browser():
        time.sleep(2)
        try:
            webbrowser.open('http://localhost:5000')
            print("🌐 Browser opened automatically\n")
        except:
            print("⚠ Could not open browser automatically")
            print("   Please visit: http://localhost:5000 manually\n")
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run the app
    print("="*70)
    print("🟢 SERVER RUNNING - Naukri Automation Web UI Active")
    print("="*70 + "\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\n✓ Server stopped by user")
except Exception as e:
    print(f"\n✗ Error: {e}")
    logger.error(f"Failed to start app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
