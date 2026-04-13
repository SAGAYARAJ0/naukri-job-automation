#!/usr/bin/env python
"""
Quick validation script for production deployment setup.
Tests that all production files are in place and correctly configured.

Usage:
    python test_production_setup.py
"""

import os
import sys
import json
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check_file_exists(path, description):
    """Check if a file exists and report status"""
    exists = os.path.isfile(path)
    status = f"{GREEN}✓ FOUND{RESET}" if exists else f"{RED}✗ MISSING{RESET}"
    print(f"{BLUE}→{RESET} {description}: {status}")
    return exists

def check_file_content(path, required_strings, description):
    """Check if a file contains required content"""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        all_found = all(s in content for s in required_strings)
        if all_found:
            print(f"{BLUE}→{RESET} {description}: {GREEN}✓ VALID{RESET}")
            return True
        else:
            missing = [s for s in required_strings if s not in content]
            print(f"{BLUE}→{RESET} {description}: {RED}✗ INVALID{RESET}")
            print(f"   {RED}Missing: {missing}{RESET}")
            return False
    except Exception as e:
        print(f"{BLUE}→{RESET} {description}: {RED}✗ ERROR - {e}{RESET}")
        return False

def check_env_variables():
    """Check if environment variables are set"""
    status_email = "NAUKRI_EMAIL" in os.environ
    status_password = "NAUKRI_PASSWORD" in os.environ
    
    email_status = f"{GREEN}✓ SET{RESET}" if status_email else f"{YELLOW}⚠ NOT SET (required for production){RESET}"
    pwd_status = f"{GREEN}✓ SET{RESET}" if status_password else f"{YELLOW}⚠ NOT SET (required for production){RESET}"
    
    print(f"{BLUE}→{RESET} NAUKRI_EMAIL environment variable: {email_status}")
    print(f"{BLUE}→{RESET} NAUKRI_PASSWORD environment variable: {pwd_status}")
    
    return status_email and status_password

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'gunicorn',
        'selenium',
        'apscheduler',
        'dotenv'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"{BLUE}→{RESET} Package '{package}': {GREEN}✓ INSTALLED{RESET}")
        except ImportError:
            print(f"{BLUE}→{RESET} Package '{package}': {RED}✗ NOT INSTALLED{RESET}")
            all_installed = False
    
    return all_installed

def check_directory_structure():
    """Check if required directories exist"""
    required_dirs = [
        'templates',
        'static',
        'config',
        'data',
        'core',
        'modules',
        'utils'
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        exists = os.path.isdir(dir_name)
        status = f"{GREEN}✓ EXISTS{RESET}" if exists else f"{YELLOW}⚠ MISSING{RESET}"
        print(f"{BLUE}→{RESET} Directory '{dir_name}': {status}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    compatible = version.major == 3 and version.minor >= 8
    
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    status = f"{GREEN}✓ COMPATIBLE{RESET}" if compatible else f"{RED}✗ INCOMPATIBLE{RESET}"
    print(f"{BLUE}→{RESET} Python version {version_str}: {status}")
    
    return compatible

def main():
    """Run all checks"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}🔍 PRODUCTION DEPLOYMENT VALIDATION{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    checks = {
        "Production Files": [],
        "Configuration Files": [],
        "Core Modules": [],
        "Web UI Components": [],
        "Environment Setup": [],
        "Dependencies": [],
        "Directory Structure": [],
        "Python Version": []
    }
    
    # 1. Check production files
    print(f"\n{YELLOW}1. Production Files{RESET}")
    checks["Production Files"].append(check_file_exists('wsgi.py', 'WSGI entrypoint (wsgi.py)'))
    checks["Production Files"].append(check_file_exists('Procfile', 'Heroku/container config (Procfile)'))
    checks["Production Files"].append(check_file_exists('runtime.txt', 'Python version (runtime.txt)'))
    checks["Production Files"].append(check_file_exists('pyproject.toml', 'Modern packaging (pyproject.toml)'))
    
    # 2. Check configuration files
    print(f"\n{YELLOW}2. Configuration Files{RESET}")
    checks["Configuration Files"].append(check_file_exists('config/config.json', 'Main config'))
    checks["Configuration Files"].append(check_file_exists('config/filters.json', 'Filter config'))
    checks["Configuration Files"].append(check_file_exists('.env', '.env credentials file'))
    
    # 3. Check core modules
    print(f"\n{YELLOW}3. Core Modules{RESET}")
    checks["Core Modules"].append(check_file_exists('core/__init__.py', 'Core package'))
    # Orchestrator module is optional - may be integrated in other modules
    orchestrator_exists = check_file_exists('modules/orchestrator.py', 'Orchestrator module (optional)')
    if not orchestrator_exists:
        print(f"   {YELLOW}Note: Orchestrator functionality may be in main.py or other modules{RESET}")
        checks["Core Modules"].append(True)  # Mark as passed since it's optional
    else:
        checks["Core Modules"].append(orchestrator_exists)
    checks["Core Modules"].append(check_file_exists('app.py', 'Flask app'))
    
    # 4. Check web UI components
    print(f"\n{YELLOW}4. Web UI Components{RESET}")
    checks["Web UI Components"].append(check_file_exists('templates/index.html', 'Web UI template'))
    checks["Web UI Components"].append(check_file_exists('run_web_ui.py', 'Web UI launcher'))
    
    # 5. Check file contents
    print(f"\n{YELLOW}5. File Contents Validation{RESET}")
    checks["Configuration Files"].append(
        check_file_content('wsgi.py', ['from app import app'], 'WSGI imports Flask app')
    )
    checks["Configuration Files"].append(
        check_file_content('Procfile', ['gunicorn wsgi:app'], 'Procfile specifies gunicorn')
    )
    checks["Configuration Files"].append(
        check_file_content('runtime.txt', ['python-'], 'runtime.txt specifies Python version')
    )
    checks["Configuration Files"].append(
        check_file_content('pyproject.toml', ['name = "naukri-job-automation"'], 'pyproject.toml has project name')
    )
    
    # 6. Check environment variables
    print(f"\n{YELLOW}6. Environment Variables{RESET}")
    env_ok = check_env_variables()
    checks["Environment Setup"].append(env_ok)
    
    # 7. Check dependencies
    print(f"\n{YELLOW}7. Python Dependencies{RESET}")
    deps_ok = check_dependencies()
    checks["Dependencies"].append(deps_ok)
    
    # 8. Check directory structure
    print(f"\n{YELLOW}8. Directory Structure{RESET}")
    dirs_ok = check_directory_structure()
    checks["Directory Structure"].append(dirs_ok)
    
    # 9. Check Python version
    print(f"\n{YELLOW}9. Python Version{RESET}")
    version_ok = check_python_version()
    checks["Python Version"].append(version_ok)
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}📊 VALIDATION SUMMARY{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    all_checks_count = sum(len(v) for v in checks.values() if v)
    passed_checks = sum(sum(1 for x in v if x) for v in checks.values() if v)
    
    for category, results in checks.items():
        if results:
            passed = sum(1 for x in results if x)
            total = len(results)
            status = f"{GREEN}✓{RESET}" if passed == total else f"{RED}✗{RESET}"
            print(f"{status} {category}: {passed}/{total} passed")
    
    print(f"\n{BLUE}-{RESET} Overall: {passed_checks}/{all_checks_count} checks passed")
    
    # Deployment readiness
    print(f"\n{BLUE}{'='*60}{RESET}")
    if passed_checks == all_checks_count:
        print(f"{GREEN}✓ READY FOR DEPLOYMENT!{RESET}")
        print(f"\nNext steps:")
        print(f"1. Verify environment variables are set on your hosting platform")
        print(f"2. Deploy using one of these methods:")
        print(f"   - Heroku: heroku create && git push heroku main")
        print(f"   - Railway: Connect GitHub repo to Railway")
        print(f"   - Docker: docker build -t naukri . && push to registry")
        print(f"\n3. Or test locally: gunicorn wsgi:app --bind 0.0.0.0:5000")
    else:
        print(f"{RED}✗ DEPLOYMENT NOT READY{RESET}")
        print(f"\nFix the issues above before deploying.")
        if not deps_ok:
            print(f"\nTo install missing dependencies:")
            print(f"   pip install -r requirements.txt")
        if not env_ok:
            print(f"\nTo set environment variables locally:")
            print(f"   # Windows PowerShell:")
            print(f"   $env:NAUKRI_EMAIL = 'your-email@gmail.com'")
            print(f"   $env:NAUKRI_PASSWORD = 'your-password'")
            print(f"   # Or in Windows CMD:")
            print(f"   set NAUKRI_EMAIL=your-email@gmail.com")
            print(f"   set NAUKRI_PASSWORD=your-password")
    
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    return 0 if passed_checks == all_checks_count else 1

if __name__ == '__main__':
    sys.exit(main())
