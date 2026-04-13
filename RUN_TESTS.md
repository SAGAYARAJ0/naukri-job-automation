# How to Test This Project

## Quick Start (5 minutes)

```bash
cd "e:\python job automation"
python test_quick.py
```

**Expected Output**: ✅ ALL TESTS PASSED! (shows summary of passed tests)

---

## Complete Testing Roadmap

### Level 1: Quick Validation (5 minutes)

**Purpose**: Verify basic system functionality without credentials

```bash
python test_quick.py
```

**What it tests**:
- ✓ All imports work correctly
- ✓ Configuration loads properly
- ✓ Logger initializes
- ✓ Config values are accessible
- ✓ All custom exceptions are defined
- ✓ Email/URL validators work
- ✓ Helper functions work
- ✓ Storage module initializes
- ✓ Filter module initializes
- ✓ Human behavior module initializes
- ✓ 30+ individual test cases

**Expected Result**: All tests show ✓, final message: **✅ ALL TESTS PASSED!**

**Passing Criteria**: 30+ tests pass, 0 failures

---

### Level 2: Component Testing (15 minutes)

**Purpose**: Test each module individually

```bash
python test_components.py
```

**What it tests**:
1. **Configuration Module**
   - Config loads from config/config.json
   - Filters load from config/filters.json
   - Settings are accessible

2. **Logger Module**
   - Logger creates correctly
   - Logs to data/logs/app.log
   - All log levels work (info, warning, error, debug)

3. **Validators**
   - Email validation (test@example.com)
   - URL validation (https://naukri.com)
   - Experience validation (3 years)
   - Keywords validation (Python, Django)

4. **Helpers**
   - Extract job ID from URL
   - Sanitize filenames
   - Timestamp generation
   - Date formatting
   - Duration formatting

5. **Storage Module**
   - Save job to JSON storage
   - Check for duplicates
   - Count applications
   - Get statistics

6. **Filter Module**
   - Filter single job
   - Calculate skill score
   - Calculate experience score
   - Batch filter jobs (3 jobs)

7. **Human Behavior**
   - Initialize with defaults
   - Generate random delays
   - Verify delay ranges

8. **Scheduler Module**
   - Create scheduler
   - Add interval job
   - Add daily job
   - Get scheduled jobs
   - Remove jobs

9. **Exception Types**
   - All 13 exception types defined
   - Exception raising works

**Expected Result**: Each test section shows ✓, ends with: **✅ ALL COMPONENT TESTS COMPLETED SUCCESSFULLY!**

**Output Location**: Console output + logs appear in data/logs/

---

### Level 3: Data & Configuration Testing (10 minutes)

**Purpose**: Verify configuration files and data structures

#### Check Configuration Files

```bash
# Verify config.json exists and is valid JSON
python -c "import json; json.load(open('config/config.json'))"
echo "✓ config.json is valid JSON"

# Verify filters.json exists and is valid JSON
python -c "import json; json.load(open('config/filters.json'))"
echo "✓ filters.json is valid JSON"
```

**Expected**: No errors, both files are valid JSON

#### Check Data Directory Structure

```bash
# List data directory
dir data\

# Check if logs directory exists
dir data\logs\
```

**Expected**: 
- `logs/` directory should exist
- `applied_jobs.json` may exist (if jobs were applied)
- `jobs.db` may exist (if SQLite storage was used)

#### Validate JSON Files

```bash
# View applied_jobs.json if it exists
python -c "import json; data = json.load(open('data/applied_jobs.json')); print(f'Jobs stored: {len(data)}')"
```

---

### Level 4: Integration Testing (30 minutes)

**Purpose**: Test module interactions (uses mocks, no real browser)

#### Test Storage Operations

```python
from modules.storage import StorageModule
import time

storage = StorageModule(storage_type='json')

# Save test job
test_id = f"test_{int(time.time())}"
storage.save_applied_job(
    test_id,
    "Test Job Title",
    "https://naukri.com/test",
    "success"
)

# Verify it was saved
assert storage.is_already_applied(test_id), "Job not saved!"
print("✓ Storage operations working")

# Check statistics
stats = storage.get_statistics()
print(f"  Total jobs: {stats['total_applications']}")
print(f"  Successful: {stats['successful']}")
```

#### Test Filter Module Logic

```python
from modules.filter import FilterModule

filter_mod = FilterModule()

# Test scoring algorithm
job = {
    "title": "Senior Python Backend Developer - 5+ years",
    "company": "TechCorp"
}

profile = {
    "skills": ["Python", "Django", "REST API"],
    "experience": 5,
    "locations": ["Bangalore"]
}

result = filter_mod.filter_job(job, profile)

assert result['score'] >= 70, f"Low score: {result['score']}"
assert result['decision'] == True, "Should approve"
print(f"✓ Filter logic working - score: {result['score']:.1f}%")
```

#### Test Exception Handling

```python
from core.exceptions import LoginException, CaptchaRequiredException

try:
    raise LoginException("Test error handling")
except LoginException as e:
    print(f"✓ Exception caught: {e}")

try:
    raise CaptchaRequiredException("CAPTCHA appeared")
except CaptchaRequiredException as e:
    print(f"✓ CAPTCHA exception caught: {e}")
```

---

### Level 5: Production Testing (20+ minutes, requires credentials)

**⚠️ IMPORTANT**: Requires valid Naukri email and password

#### Step 1: Configure Credentials

Edit `config/config.json`:

```json
{
  "naukri": {
    "email": "your-email@example.com",
    "password": "your-password"
  }
}
```

#### Step 2: Test Login Only (5 minutes)

```python
from modules.login import LoginModule
from core.driver_manager import get_driver_manager

driver = get_driver_manager().get_driver()
login = LoginModule(driver)

try:
    login.login("your-email@example.com", "your-password")
    print("✓ Login successful!")
    
    # Verify logged in
    assert "home" in driver.current_url or "mnjuser" in driver.current_url
    print("✓ Currently on Naukri dashboard")
    
except Exception as e:
    print(f"✗ Login failed: {e}")
finally:
    get_driver_manager().close_driver()
```

**Expected**: Browser opens, logs in, stays on Naukri dashboard

#### Step 3: Test Search (10 minutes)

```python
from modules.search import SearchModule

search = SearchModule(driver)

jobs = search.search_jobs(
    keywords="Python",
    location="Bangalore",
    experience=3,
    max_pages=2
)

print(f"✓ Found {len(jobs)} jobs")
for job in jobs[:3]:
    print(f"  - {job['title']} at {job['company']}")

assert len(jobs) > 0, "No jobs found!"
```

**Expected**: Returns list of 10+ job listings

#### Step 4: Test Filtering (5 minutes)

```python
from modules.filter import FilterModule

filter_mod = FilterModule()

filtered = filter_mod.batch_filter(jobs, {
    "skills": ["Python", "Django"],
    "experience": 3
})

print(f"✓ Filtered {len(filtered)}/{len(jobs)} jobs")

for job in filtered[:3]:
    print(f"  - {job['title']} (score: {job.get('filter_score', 0):.1f}%)")
```

**Expected**: 30-50% of jobs pass filtering

#### Step 5: Full End-to-End (without applying) (20 minutes)

```python
from main import Orchestrator

orchestrator = Orchestrator()

summary = orchestrator.run_automation(
    email="your-email@example.com",
    password="your-password",
    keywords="Python",
    location="Bangalore",
    experience=3,
    max_pages=1,
    apply=False  # Don't actually apply
)

print(f"\n===== AUTOMATION SUMMARY =====")
print(f"Jobs found: {summary['jobs_found']}")
print(f"Jobs filtered: {summary['jobs_filtered']}")
print(f"Success rate: {summary['success_rate']:.1f}%")
```

**Expected**: Shows summary of jobs found and filtered

---

## Test Commands Reference

| Test | Command | Time | Credentials | Files Modified |
|------|---------|------|-------------|-----------------|
| Quick | `python test_quick.py` | 5min | ❌ No | ❌ None |
| Components | `python test_components.py` | 15min | ❌ No | ✅ data/applied_jobs.json |
| Configuration | Manual JSON validation | 10min | ❌ No | ❌ None |
| Integration | Python snippets | 30min | ❌ No | ✅ data/ |
| Production | Full orchestrator | 20min+ | ✅ **Yes** | ✅ data/, Naukri account |

---

## Expected Test Output

### test_quick.py Output:
```
======================================================================
QUICK VALIDATION TESTS
======================================================================

TEST 1: Module Imports
✓ core.exceptions
✓ core.logger
✓ core.config_manager
...
Imports: 8/8 passed ✓

TEST 2: Configuration Loading
✓ Config loads correctly
✓ Filters load correctly
Config: 2/2 passed ✓

...

======================================================================
✅ ALL TESTS PASSED! (30/30)
======================================================================
```

### test_components.py Output:
```
======================================================================
COMPONENT TESTING
======================================================================

TEST 1: Configuration Module
✓ Config loaded
  - Naukri login URL: https://www.naukri.com/...
  - Email selector: #usernameField
  ...

TEST 2: Logger Module
✓ Logger created
✓ Messages logged to data/logs/app.log

...

======================================================================
✅ ALL COMPONENT TESTS COMPLETED SUCCESSFULLY!
======================================================================
```

---

## Troubleshooting Test Failures

### "ModuleNotFoundError: No module named 'selenium'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: config/config.json not found"

**Solution**: Check file exists
```bash
dir config\
```

If missing, run:
```bash
python -c "from core.config_manager import get_config; get_config()"
```

### "FileNotFoundError: data/ directory not found"

**Solution**: Create data directory
```bash
mkdir data
mkdir data\logs
```

### Storage tests fail with "applied_jobs.json not found"

**Solution**: This is normal on first run. StorageModule will create it. Just run tests again.

### Filter module shows "NLTK data not found"

**Solution**: Download NLTK data
```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

### Production test fails at login

**Possible causes**:
- Wrong email/password in config.json
- 2FA enabled on account (pause for manual entry)
- IP blocked by Naukri
- Bot detection triggered

**Solution**: 
- Verify credentials are correct
- Check logs in data/logs/
- Try from different network
- Increase delays in config.json

---

## Testing Best Practices

### 1. **Test Order**
   - Always run test_quick.py first
   - If passes, run test_components.py
   - If both pass, attempt production tests

### 2. **Isolation**
   - Each test level is independent
   - Can skip levels (e.g., go straight to Level 4)
   - Production tests don't affect dev environment

### 3. **Data Safety**
   - test_quick.py and test_components.py save test data to storage
   - Safe to delete data/applied_jobs.json between test runs
   - Never delete data/logs/ (historical records)

### 4. **Debugging Failed Tests**
   1. Check data/logs/app.log for error details
   2. Check data/logs/error.log for exceptions
   3. Run failing test again with verbose output
   4. Add temporary print statements for debugging

### 5. **Before Production**
   - ✅ test_quick.py passes
   - ✅ test_components.py passes
   - ✅ config.json has real credentials
   - ✅ tested login with real account
   - ✅ reviewed data/logs/ for errors

---

## Next Steps After Testing

| Result | Next Action |
|--------|------------|
| ✅ All tests pass | Run `python main.py` for single execution |
| ⚠️ Some tests fail | Check troubleshooting section above |
| ❌ Critical failure | Review config.json and logs/ directory |
| ✅ Ready for production | Run `python run_scheduled.py` for scheduling |

---

## Getting Help

### View Logs
```bash
# View all logs
cat data/logs/app.log

# View only errors
cat data/logs/error.log

# View last 50 lines
tail -50 data/logs/app.log
```

### Check Configuration
```python
from core.config_manager import get_config
config = get_config()
print(config.config_data)
```

### List Scheduled Jobs
```python
from modules.scheduler import SchedulerModule
scheduler = SchedulerModule()
for job in scheduler.get_jobs():
    print(job)
```

---

**Last Updated**: Implementation Phase 5 (Complete)
**Status**: ✅ Ready for Testing
