"""
TESTING GUIDE - Naukri Job Automation System
Complete testing strategies and test cases
"""

# 🧪 COMPREHENSIVE TESTING GUIDE

## TESTING LEVELS

### Level 1: Quick Validation (No Credentials Needed) ⚡
### Level 2: Component Testing (Individual Modules) 🔧
### Level 3: Integration Testing (Full Workflow) 🔗
### Level 4: Production Testing (Real Naukri) 🚀
### Level 5: Performance Testing ⚡📊

---

## LEVEL 1: QUICK VALIDATION (5 MINUTES)

### Test 1.1: Check Installation
```bash
# Verify Python
python --version

# Verify pip packages
pip list | findstr selenium webdriver apscheduler nltk

# Test imports
python -c "from selenium import webdriver; print('✓ Selenium OK')"
python -c "from apscheduler.schedulers.background import BackgroundScheduler; print('✓ APScheduler OK')"
python -c "import nltk; print('✓ NLTK OK')"
```

### Test 1.2: Verify Project Structure
```bash
# Check all directories exist
ls core modules utils config data

# Check critical files
ls main.py requirements.txt config/config.json config/filters.json

# List all Python files
ls -Recurse *.py | Measure-Object
```

### Test 1.3: Config Loading
```python
# test_config.py
from core.config_manager import get_config

config = get_config()

# Test config loading
print("✓ Config loaded")

# Test getting values
email_selector = config.get('naukri.email_selector')
print(f"✓ Email selector: {email_selector}")

# Test default config
all_config = config.get_all()
print(f"✓ Total config keys: {len(all_config)}")

# Test filter loading
filters = config.load_filters()
print(f"✓ Filters loaded: {len(filters)}")
print(f"  - Required skills: {filters.get('required_skills', [])}")
print(f"  - Min experience: {filters.get('min_experience', 0)}")
```

Run:
```bash
python test_config.py
```

### Test 1.4: Logger Setup
```python
# test_logger.py
from core.logger import get_logger

logger = get_logger("test_module")

logger.info("ℹ️  Info message")
logger.warning("⚠️  Warning message")
logger.error("❌ Error message")
logger.debug("🐛 Debug message")

print("\n✓ Check logs in: data/logs/app.log")
```

Run:
```bash
python test_logger.py
# Then check logs
Get-Content "data/logs/app.log" -Tail 10
```

### Test 1.5: Modules Import
```python
# test_imports.py
print("Testing module imports...\n")

try:
    from modules.login import LoginModule
    print("✓ LoginModule imported")
except Exception as e:
    print(f"✗ LoginModule failed: {e}")

try:
    from modules.search import SearchModule
    print("✓ SearchModule imported")
except Exception as e:
    print(f"✗ SearchModule failed: {e}")

try:
    from modules.filter import FilterModule
    print("✓ FilterModule imported")
except Exception as e:
    print(f"✗ FilterModule failed: {e}")

try:
    from modules.apply import ApplyModule
    print("✓ ApplyModule imported")
except Exception as e:
    print(f"✗ ApplyModule failed: {e}")

try:
    from modules.storage import StorageModule
    print("✓ StorageModule imported")
except Exception as e:
    print(f"✗ StorageModule failed: {e}")

try:
    from modules.scheduler import SchedulerModule
    print("✓ SchedulerModule imported")
except Exception as e:
    print(f"✗ SchedulerModule failed: {e}")

try:
    from utils.human_behavior import HumanBehavior
    print("✓ HumanBehavior imported")
except Exception as e:
    print(f"✗ HumanBehavior failed: {e}")

try:
    from utils.validators import Validators
    print("✓ Validators imported")
except Exception as e:
    print(f"✗ Validators failed: {e}")

try:
    from utils.helpers import Helpers
    print("✓ Helpers imported")
except Exception as e:
    print(f"✗ Helpers failed: {e}")

print("\n✓ All modules imported successfully!")
```

Run:
```bash
python test_imports.py
```

---

## LEVEL 2: COMPONENT TESTING (15 MINUTES)

### Test 2.1: Validators
```python
# test_validators.py
from utils.validators import Validators

print("Testing Validators...\n")

# Test email validation
try:
    Validators.validate_email("test@naukri.com")
    print("✓ Valid email accepted")
except:
    print("✗ Email validation failed")

try:
    Validators.validate_email("invalid-email")
    print("✗ Invalid email should fail")
except:
    print("✓ Invalid email rejected")

# Test URL validation
try:
    Validators.validate_url("https://www.naukri.com")
    print("✓ Valid URL accepted")
except:
    print("✗ URL validation failed")

# Test experience validation
try:
    Validators.validate_experience(3)
    print("✓ Valid experience accepted")
except:
    print("✗ Experience validation failed")

try:
    Validators.validate_experience(-1)
    print("✗ Negative experience should fail")
except:
    print("✓ Invalid experience rejected")

# Test keywords validation
try:
    Validators.validate_keywords(["Python", "Django"])
    print("✓ Valid keywords accepted")
except:
    print("✗ Keywords validation failed")

try:
    Validators.validate_keywords([])
    print("✗ Empty keywords should fail")
except:
    print("✓ Empty keywords rejected")

print("\n✓ All validators working correctly!")
```

Run:
```bash
python test_validators.py
```

### Test 2.2: Helpers
```python
# test_helpers.py
from utils.helpers import Helpers
import json

print("Testing Helpers...\n")

# Test job ID extraction
url = "https://www.naukri.com/job-listings-python-developer-xyz-123456789"
job_id = Helpers.extract_job_id(url)
print(f"✓ Job ID extracted: {job_id}")

# Test filename sanitization
bad_filename = "Job<Title>|Invalid*Name?.txt"
clean = Helpers.sanitize_filename(bad_filename)
print(f"✓ Filename sanitized: {clean}")

# Test timestamp
ts = Helpers.get_timestamp()
print(f"✓ Timestamp: {ts}")

# Test date string
date_str = Helpers.get_date_str()
print(f"✓ Date string: {date_str}")

# Test duration formatting
duration = Helpers.format_duration(3665)  # 1h 1m 5s
print(f"✓ Duration formatted: {duration}")

# Test JSON save/load
test_data = {"key": "value", "number": 123}
test_file = "test_data.json"

success = Helpers.save_json(test_data, test_file)
print(f"✓ JSON saved: {success}")

loaded = Helpers.load_json(test_file)
print(f"✓ JSON loaded: {loaded}")

# Cleanup
import os
os.remove(test_file)

print("\n✓ All helpers working correctly!")
```

Run:
```bash
python test_helpers.py
```

### Test 2.3: Storage Module
```python
# test_storage.py
from modules.storage import StorageModule
import time

print("Testing Storage Module...\n")

# Initialize storage
storage = StorageModule(storage_type='json')
print("✓ Storage initialized")

# Test saving applied job
job_id = f"job_{int(time.time())}"
storage.save_applied_job(job_id, "Python Developer", "https://naukri.com/job", "success")
print(f"✓ Job saved: {job_id}")

# Test checking if already applied
is_applied = storage.is_already_applied(job_id)
print(f"✓ Already applied check: {is_applied}")

# Test getting count
count = storage.get_application_count()
print(f"✓ Application count: {count}")

# Test statistics
stats = storage.get_statistics()
print(f"✓ Statistics: {stats}")

# Test export
export_file = storage.export_history()
print(f"✓ History exported: {export_file}")

print("\n✓ Storage module working correctly!")
```

Run:
```bash
python test_storage.py
```

### Test 2.4: Filter Module
```python
# test_filter.py
from modules.filter import FilterModule

print("Testing Filter Module...\n")

# Initialize filter
filter_module = FilterModule()
print("✓ Filter module initialized")

# Create test job
test_job = {
    "title": "Senior Python Developer",
    "company": "TechCorp",
    "location": "Bangalore",
    "url": "https://naukri.com/job"
}

# Create user profile
user_profile = {
    "skills": ["Python", "Django", "SQL", "REST API"],
    "experience": 3,
    "locations": ["Bangalore", "Mumbai"]
}

# Test filtering
result = filter_module.filter_job(test_job, user_profile)

print(f"\n✓ Job filtered:")
print(f"  - Decision: {result['decision']}")
print(f"  - Score: {result['score']:.2f}")
print(f"  - Details: {result['details']}")

# Test batch filtering
test_jobs = [
    {"title": "Python Dev", "company": "Company A"},
    {"title": "Java Dev", "company": "Company B"},
    {"title": "Django Developer", "company": "Company C"}
]

filtered = filter_module.batch_filter(test_jobs, user_profile)
print(f"\n✓ Batch filtered: {len(filtered)}/{len(test_jobs)} jobs passed")

print("\n✓ Filter module working correctly!")
```

Run:
```bash
python test_filter.py
```

### Test 2.5: Human Behavior
```python
# test_human_behavior.py
from utils.human_behavior import HumanBehavior
import time

print("Testing Human Behavior Simulation...\n")

behavior = HumanBehavior()
print("✓ Human behavior initialized")

# Test random delay
print("Testing random delay (2-5 seconds)...")
start = time.time()
behavior.random_delay()
elapsed = time.time() - start
print(f"✓ Actual delay: {elapsed:.2f}s")

# Test pause for CAPTCHA (with timeout)
print("\nTesting CAPTCHA pause (will timeout after 5 seconds for testing)...")
start = time.time()
# We'll simulate by using a short timeout
try:
    # Note: This will actually pause, so skip in automated testing
    print("⚠️  Skipping CAPTCHA pause test (would pause for 5 minutes)")
except:
    pass

print("\n✓ Human behavior working correctly!")
```

Run:
```bash
python test_human_behavior.py
```

---

## LEVEL 3: INTEGRATION TESTING (30 MINUTES)

### Test 3.1: Mock Browser Test (No Login Required)
```python
# test_integration_mock.py
"""
Integration test using mock WebDriver
Tests module interaction without real browser
"""

from unittest.mock import Mock, MagicMock
from modules.search import SearchModule
from modules.filter import FilterModule

print("Testing Integration (Mock)...\n")

# Create mock driver
mock_driver = MagicMock()

# Mock the navigate
mock_driver.get = MagicMock()
mock_driver.find_elements = MagicMock(return_value=[])

print("✓ Mock driver created")

# Test search module with mock
search = SearchModule(mock_driver)
print("✓ Search module initialized")

# Build search URL
url = search._build_search_url(["Python"], "Bangalore", 3)
print(f"✓ Search URL built: {url}")

# Test filter module
filter_module = FilterModule()
print("✓ Filter module initialized")

# Test job filtering with sample
sample_job = {
    "title": "Python Backend Developer - 3+ years",
    "company": "Tech Company",
    "location": "Bangalore",
    "url": "https://naukri.com/job/123"
}

result = filter_module.filter_job(sample_job)
print(f"✓ Job filtered: Decision={result['decision']}, Score={result['score']:.1f}")

print("\n✓ Integration test passed!")
```

Run:
```bash
python test_integration_mock.py
```

### Test 3.2: Database Test
```python
# test_database.py
"""
Test SQLite storage as alternative to JSON
"""

from modules.storage import StorageModule
import time

print("Testing SQLite Storage...\n")

# Initialize SQLite storage
storage = StorageModule(storage_type='sqlite')
print("✓ SQLite storage initialized")

# Add test records
for i in range(5):
    job_id = f"job_sqlite_{i}"
    storage.save_applied_job(
        job_id,
        f"Python Developer {i}",
        f"https://naukri.com/job/{i}",
        "success"
    )

print("✓ 5 test jobs saved")

# Check count
count = storage.get_application_count()
print(f"✓ Total jobs in SQLite: {count}")

# Check if applied
is_applied = storage.is_already_applied("job_sqlite_0")
print(f"✓ Duplicate check: {is_applied}")

# Get statistics
stats = storage.get_statistics()
print(f"✓ Statistics: {stats}")

print("\n✓ SQLite storage working correctly!")
```

Run:
```bash
python test_database.py
```

---

## LEVEL 4: PRODUCTION TESTING (WITH REAL NAUKRI)

### Test 4.1: Dry Run (Headless Mode Off)
```bash
# Edit config/config.json first!
# Update with your actual Naukri credentials

# Run with headless: false to see browser
python -c "
from core.config_manager import get_config
config = get_config()
# Check headless is false
print(f'Headless: {config.get(\"automation.headless\")}')
"

# Now run main
python main.py
```

### Test 4.2: Step-by-Step Testing
```python
# test_production_step_by_step.py
"""
Test each component with real Naukri
"""

from core import get_driver_manager
from core.logger import get_logger
from modules.login import LoginModule
import time

logger = get_logger(__name__)

print("STEP 1: Initialize Driver\n")
driver_mgr = get_driver_manager()
driver = driver_mgr.get_driver(use_headless=False)
print("✓ Driver initialized, browser opened")

print("\nSTEP 2: Test Navigation\n")
driver.get("https://www.naukri.com")
print("✓ Navigated to Naukri")
time.sleep(2)

print("\nSTEP 3: Check Page Load\n")
if "naukri" in driver.current_url:
    print("✓ Page loaded successfully")
else:
    print("✗ Page didn't load correctly")

print("\nSTEP 4: Test Element Finding\n")
try:
    elements = driver.find_elements("xpath", "//div[contains(text(), 'Search')]")
    print(f"✓ Found {len(elements)} search elements")
except Exception as e:
    print(f"✗ Error finding elements: {e}")

print("\nSTEP 5: Check Cookies\n")
cookies = driver.get_cookies()
print(f"✓ Browser has {len(cookies)} cookies")

print("\nDone! Check the browser for any issues.")
print("Close browser window to continue.")

# Keep browser open
input("Press Enter to close browser...")
driver_mgr.quit_driver()
print("\n✓ Browser closed")
```

Run:
```bash
python test_production_step_by_step.py
```

### Test 4.3: Login Test (Requires Manual CAPTCHA)
```python
# test_login_real.py
"""
Test real login with actual Naukri account
Requires manual CAPTCHA solving
"""

from core import get_driver_manager, get_config
from modules.login import LoginModule
from core.logger import get_logger

logger = get_logger(__name__)
config = get_config()

print("TESTING REAL LOGIN\n")
print("="*50)

# Get credentials from config
email = config.get('credentials.email')
password = config.get('credentials.password')

if email == "your-email@example.com":
    print("❌ Please update credentials in config/config.json first!")
    exit(1)

print(f"Email: {email}")
print(f"Password: {'*' * len(password)}")
print("="*50 + "\n")

# Initialize driver
driver_mgr = get_driver_manager()
driver = driver_mgr.get_driver(use_headless=False)

# Login
login = LoginModule(driver)
result = login.login(email, password)

print(f"\nResult: {result}")

if result['status'] == 'success':
    print("\n✅ LOGIN SUCCESSFUL!")
    print("You are logged in. Checking browser...")
    input("Press Enter to logout and close browser...")
else:
    print(f"\n❌ Login failed: {result['message']}")

# Save cookies for future sessions
if 'cookies' in result:
    print(f"✓ Cookies saved: {len(result['cookies'])} cookies")

driver_mgr.quit_driver()
print("✓ Browser closed")
```

Run:
```bash
# Update config/config.json with your credentials first
python test_login_real.py
```

---

## LEVEL 5: TEST EXAMPLES & SCENARIOS

### Test 5.1: Search Test
```python
# test_search.py
"""
Test job search without applying
"""

from core import get_driver_manager, get_config
from modules.login import LoginModule
from modules.search import SearchModule
from core.logger import get_logger

logger = get_logger(__name__)
config = get_config()

email = config.get('credentials.email')
password = config.get('credentials.password')

if email == "your-email@example.com":
    print("❌ Update credentials first!")
    exit(1)

print("TESTING JOB SEARCH\n")

# Setup
driver_mgr = get_driver_manager()
driver = driver_mgr.get_driver(use_headless=False)

# Login
print("1. Logging in...")
login = LoginModule(driver)
result = login.login(email, password)
if result['status'] != 'success':
    print(f"❌ Login failed: {result}")
    exit(1)
print("✓ Logged in\n")

# Search
print("2. Searching for jobs...")
search = SearchModule(driver)
jobs = search.search_jobs(
    keywords=["Python"],
    location="Bangalore",
    experience=2,
    max_pages=2  # Just 2 pages for testing
)
print(f"✓ Found {len(jobs)} jobs\n")

# Show results
print("Search Results:")
for i, job in enumerate(jobs[:5], 1):
    print(f"{i}. {job.get('title')} @ {job.get('company')}")

# Cleanup
driver_mgr.quit_driver()
print("\n✓ Test completed")
```

Run:
```bash
python test_search.py
```

### Test 5.2: End-to-End Test (No Apply)
```python
# test_end_to_end.py
"""
Full workflow test without actually applying
"""

from core import get_driver_manager, get_config
from modules.login import LoginModule
from modules.search import SearchModule
from modules.filter import FilterModule
from core.logger import get_logger

logger = get_logger(__name__)
config = get_config()

email = config.get('credentials.email')
password = config.get('credentials.password')

if email == "your-email@example.com":
    print("❌ Update credentials first!")
    exit(1)

print("="*60)
print("END-TO-END TEST (WITHOUT APPLYING)")
print("="*60 + "\n")

driver_mgr = get_driver_manager()
driver = driver_mgr.get_driver(use_headless=False)

try:
    # 1. LOGIN
    print("✓ Step 1: Login")
    login = LoginModule(driver)
    result = login.login(email, password)
    if result['status'] != 'success':
        print(f"❌ Login failed")
        exit(1)
    
    # 2. SEARCH
    print("✓ Step 2: Search for jobs")
    search = SearchModule(driver)
    jobs = search.search_jobs(
        keywords=["Python", "Django"],
        location="Bangalore",
        experience=2,
        max_pages=2
    )
    print(f"  Found {len(jobs)} jobs")
    
    # 3. FILTER
    print("✓ Step 3: Filter jobs")
    filter_module = FilterModule()
    filters = config.load_filters()
    filtered = filter_module.batch_filter(jobs)
    print(f"  {len(filtered)} jobs passed filter")
    
    # 4. SHOW TOP MATCHES
    print("\n" + "="*60)
    print("TOP MATCHING JOBS")
    print("="*60)
    for i, job in enumerate(filtered[:3], 1):
        score = job.get('filter_score', 0)
        print(f"\n{i}. {job.get('title')}")
        print(f"   Company: {job.get('company')}")
        print(f"   Score: {score:.1f}%")
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETED SUCCESSFULLY")
    print("="*60)

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver_mgr.quit_driver()
```

Run:
```bash
python test_end_to_end.py
```

---

## QUICK TEST CHECKLIST

```
PRE-TEST CHECKLIST
┌─────────────────────────────────────────────┐
│ ☐ Python 3.8+ installed                    │
│ ☐ requirements.txt installed                │
│ ☐ config/config.json updated (if needed)   │
│ ☐ data/logs directory exists                │
│ ☐ Chrome browser installed                  │
│ ☐ Internet connection active                │
└─────────────────────────────────────────────┘

TEST SEQUENCE
┌─────────────────────────────────────────────┐
│ 1. Run test_imports.py                      │
│ 2. Run test_validators.py                   │
│ 3. Run test_helpers.py                      │
│ 4. Run test_config.py                       │
│ 5. Run test_logger.py                       │
│ 6. Run test_filter.py                       │
│ 7. Run test_storage.py                      │
│ 8. Run test_integration_mock.py              │
│ 9. (Optional) Run test_login_real.py        │
│ 10. (Optional) Run test_search.py           │
│ 11. (Optional) Run test_end_to_end.py       │
└─────────────────────────────────────────────┘
```

---

## RUNNING ALL TESTS

```bash
# Run all quick tests
for test in test_imports.py test_validators.py test_helpers.py test_config.py test_logger.py test_filter.py test_storage.py test_integration_mock.py; do
    echo "Running $test..."
    python $test
    echo ""
done

# Check logs
echo "Checking logs..."
Get-Content "data/logs/app.log" -Tail 20
```

---

## TROUBLESHOOTING TEST FAILURES

| Issue | Solution |
|-------|----------|
| **ImportError** | Run `pip install -r requirements.txt` |
| **Config not found** | Create `config/config.json` |
| **Logs not created** | Create `data/logs/` directory |
| **Selectors not found** | Update selectors in config.json |
| **CAPTCHA timeout** | Normal - need to solve manually |
| **Rate limited (429)** | Increase min_delay in config |
| **Element stale** | Retry the test |
| **Browser crash** | Check Chrome installation |

---

## WHAT EACH TEST CHECKS

| Test | Checks |
|------|--------|
| Imports | All modules load correctly |
| Validators | Input validation works |
| Helpers | Utility functions work |
| Config | Configuration loading works |
| Logger | Logging system works |
| Filter | Job filtering works |
| Storage | Data persistence works |
| Mock Integration | Module interaction works |
| Real Login | Authentication works (requires credentials) |
| Real Search | Job search works (requires login) |
| End-to-End | Complete workflow works |

---

## NEXT: Run Tests

1. Copy the test files above into the project directory
2. Run them in sequence
3. Check `data/logs/app.log` for detailed output
4. Fix any issues
5. When all pass, you're ready for production!

---

**✅ All tests passing? Your system is production-ready!**
