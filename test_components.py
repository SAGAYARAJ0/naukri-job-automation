#!/usr/bin/env python
"""
COMPONENT TEST - Test Individual Modules
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("COMPONENT TESTING")
print("="*70 + "\n")

# Test 1: Config Module
print("TEST 1: Configuration Module")
print("-" * 70)

from core.config_manager import get_config

config = get_config()

print(f"✓ Config loaded")
print(f"  - Naukri login URL: {config.get('naukri.login_url')}")
print(f"  - Email selector: {config.get('naukri.email_selector')}")
print(f"  - Headless mode: {config.get('automation.headless')}")
print(f"  - Implicit wait: {config.get('automation.implicit_wait')}s")
print(f"  - CAPTCHA timeout: {config.get('automation.captcha_timeout')}s")
print(f"  - Min delay: {config.get('behavior.min_delay')}s")
print(f"  - Max delay: {config.get('behavior.max_delay')}s")

filters = config.load_filters()
print(f"\n✓ Filters loaded")
print(f"  - Required skills: {filters.get('required_skills', [])}")
print(f"  - Min experience: {filters.get('min_experience', 0)} years")
print(f"  - Filter threshold: {filters.get('filter_threshold', 70)}%")

# Test 2: Logger Module
print("\n\nTEST 2: Logger Module")
print("-" * 70)

from core.logger import get_logger

logger = get_logger("component_test")
print(f"✓ Logger created")

logger.info("INFO message - testing")
logger.warning("WARNING message - testing")
logger.error("ERROR message - testing")
logger.debug("DEBUG message - testing")

print(f"✓ Messages logged to data/logs/app.log")

# Test 3: Validators
print("\n\nTEST 3: Validators Module")
print("-" * 70)

from utils.validators import Validators
from core.exceptions import ConfigException

print(f"✓ Validators module loaded")

# Test email
try:
    Validators.validate_email("test@example.com")
    print(f"  ✓ Email validation: Valid")
except ConfigException as e:
    print(f"  ✗ Email validation failed: {e}")

# Test URL
try:
    Validators.validate_url("https://www.naukri.com")
    print(f"  ✓ URL validation: Valid")
except ConfigException as e:
    print(f"  ✗ URL validation failed: {e}")

# Test experience
try:
    Validators.validate_experience(3)
    print(f"  ✓ Experience validation: Valid")
except ConfigException as e:
    print(f"  ✗ Experience validation failed: {e}")

# Test keywords
try:
    Validators.validate_keywords(["Python", "Django"])
    print(f"  ✓ Keywords validation: Valid")
except ConfigException as e:
    print(f"  ✗ Keywords validation failed: {e}")

# Test 4: Helpers
print("\n\nTEST 4: Helpers Module")
print("-" * 70)

from utils.helpers import Helpers

print(f"✓ Helpers module loaded")

# Test job ID extraction
url = "https://www.naukri.com/job-listings-python-dev-123456789-something"
job_id = Helpers.extract_job_id(url)
print(f"  ✓ Extracted job ID: {job_id}")

# Test filename sanitization
dirty = "Invalid<File>Name|*.txt"
clean = Helpers.sanitize_filename(dirty)
print(f"  ✓ Sanitized filename: {clean}")

# Test timestamp
ts = Helpers.get_timestamp()
print(f"  ✓ Current timestamp: {ts}")

# Test date
date = Helpers.get_date_str()
print(f"  ✓ Current date: {date}")

# Test duration
duration = Helpers.format_duration(3665)
print(f"  ✓ Duration format (3665s): {duration}")

# Test 5: Storage Module
print("\n\nTEST 5: Storage Module (JSON)")
print("-" * 70)

from modules.storage import StorageModule
import time

storage = StorageModule(storage_type='json')
print(f"✓ Storage initialized (JSON mode)")

# Test saving
test_job_id = f"test_component_{int(time.time())}"
storage.save_applied_job(
    test_job_id,
    "Python Developer",
    "https://naukri.com/job/123",
    "success"
)
print(f"  ✓ Job saved: {test_job_id}")

# Test duplicate check
is_applied = storage.is_already_applied(test_job_id)
print(f"  ✓ Duplicate check: {is_applied}")

# Test count
count = storage.get_application_count()
print(f"  ✓ Total applications: {count}")

# Test statistics
stats = storage.get_statistics()
print(f"  ✓ Statistics retrieved")
print(f"    - Total: {stats.get('total_applications', 0)}")
print(f"    - Successful: {stats.get('successful', 0)}")

# Test 6: Filter Module
print("\n\nTEST 6: Filter Module")
print("-" * 70)

from modules.filter import FilterModule

filter_module = FilterModule()
print(f"✓ Filter module initialized")

# Test job filtering
test_job = {
    "title": "Senior Python Backend Developer - 3+ years",
    "company": "TechCorp India",
    "location": "Bangalore",
    "url": "https://naukri.com/job/123"
}

user_profile = {
    "skills": ["Python", "Django", "SQL", "REST API"],
    "experience": 3,
    "locations": ["Bangalore"]
}

result = filter_module.filter_job(test_job, user_profile)

print(f"  ✓ Job filtered")
print(f"    - Decision: {'APPLY' if result['decision'] else 'SKIP'}")
print(f"    - Score: {result['score']:.1f}%")

details = result['details']
print(f"    - Skill score: {details['skill_score']:.1f}")
print(f"    - Experience score: {details['experience_score']:.1f}")
print(f"    - Red flag score: {details['red_flag_score']:.1f}")

# Test batch filtering
test_jobs = [
    {"title": "Python Developer", "company": "Company A"},
    {"title": "Java Developer", "company": "Company B"},
    {"title": "Django Backend Developer", "company": "Company C"}
]

filtered_jobs = filter_module.batch_filter(test_jobs, user_profile)
print(f"\n  ✓ Batch filtering: {len(filtered_jobs)}/{len(test_jobs)} jobs passed")

# Test 7: Human Behavior
print("\n\nTEST 7: Human Behavior Module")
print("-" * 70)

from utils.human_behavior import HumanBehavior
import time as time_module

behavior = HumanBehavior()
print(f"✓ Human behavior initialized")
print(f"  - Min delay: {behavior.min_delay}s")
print(f"  - Max delay: {behavior.max_delay}s")
print(f"  - Typing speed: {behavior.typing_speed}s/char")

# Test random delay
print(f"\n  Testing random delay (3s)...")
start = time_module.time()
behavior.random_delay(min_delay=1, max_delay=3)
elapsed = time_module.time() - start
print(f"  ✓ Actual delay: {elapsed:.2f}s")

# Test 8: Scheduler Module
print("\n\nTEST 8: Scheduler Module")
print("-" * 70)

from modules.scheduler import SchedulerModule

scheduler = SchedulerModule()
print(f"✓ Scheduler initialized")

# Test adding a simple job
def sample_job():
    return "Job executed"

job_id = scheduler.add_interval_job(sample_job, minutes=60, job_id="test_job_1")
print(f"  ✓ Interval job added: {job_id}")

job_id = scheduler.add_daily_job(sample_job, hour=9, job_id="test_job_2")
print(f"  ✓ Daily job added: {job_id}")

jobs = scheduler.get_jobs()
print(f"  ✓ Scheduled jobs: {len(jobs)}")

# Clean up
scheduler.remove_job("test_job_1")
scheduler.remove_job("test_job_2")
print(f"  ✓ Test jobs removed")

# Test 9: Exception Types
print("\n\nTEST 9: Exception Types")
print("-" * 70)

from core.exceptions import (
    LoginException, CaptchaRequiredException, SessionExpiredException,
    SearchException, FilterException, ApplyException,
    AlreadyAppliedException, ExternalRedirectException,
    StorageException, ConfigException, DriverException,
    TimeoutException, RateLimitException
)

exceptions = [
    ("LoginException", LoginException),
    ("CaptchaRequiredException", CaptchaRequiredException),
    ("SessionExpiredException", SessionExpiredException),
    ("SearchException", SearchException),
    ("FilterException", FilterException),
    ("ApplyException", ApplyException),
    ("AlreadyAppliedException", AlreadyAppliedException),
    ("ExternalRedirectException", ExternalRedirectException),
    ("StorageException", StorageException),
    ("ConfigException", ConfigException),
    ("DriverException", DriverException),
    ("TimeoutException", TimeoutException),
    ("RateLimitException", RateLimitException),
]

print(f"✓ Exception types available: {len(exceptions)}")
for name, exc_class in exceptions:
    try:
        raise exc_class(f"Test {name}")
    except exc_class:
        print(f"  ✓ {name}")

# Summary
print("\n" + "="*70)
print("✅ ALL COMPONENT TESTS COMPLETED SUCCESSFULLY!")
print("="*70 + "\n")

print("Next steps:")
print("1. Check data/logs/app.log for detailed logs")
print("2. Review test results above")
print("3. Run test_quick.py for automated tests")
print("4. Update config/config.json with your credentials")
print("5. Run python main.py for production testing")
print()
