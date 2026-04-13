#!/usr/bin/env python
"""
QUICK TEST SUITE - Naukri Automation
Run this to verify all components work
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("NAUKRI AUTOMATION - QUICK TEST SUITE")
print("="*70 + "\n")

test_results = {
    'passed': 0,
    'failed': 0,
    'errors': []
}

def test(name, func):
    """Run a test and track results."""
    print(f"Testing: {name}...", end=" ")
    try:
        func()
        print("✓")
        test_results['passed'] += 1
    except AssertionError as e:
        print(f"✗ (Assertion: {e})")
        test_results['failed'] += 1
        test_results['errors'].append((name, str(e)))
    except Exception as e:
        print(f"✗ (Error: {e})")
        test_results['failed'] += 1
        test_results['errors'].append((name, str(e)))

# ============================================================================
# TEST IMPORTS
# ============================================================================

print("1. TESTING IMPORTS")
print("-" * 70)

def test_core_imports():
    from core.logger import get_logger
    from core.config_manager import get_config
    from core.exceptions import LoginException
    get_logger("test")
    get_config()

test("Core imports", test_core_imports)

def test_module_imports():
    from modules.login import LoginModule
    from modules.search import SearchModule
    from modules.filter import FilterModule
    from modules.apply import ApplyModule
    from modules.storage import StorageModule
    from modules.scheduler import SchedulerModule

test("Module imports", test_module_imports)

def test_utils_imports():
    from utils.human_behavior import HumanBehavior
    from utils.validators import Validators
    from utils.helpers import Helpers

test("Utils imports", test_utils_imports)

# ============================================================================
# TEST CONFIGURATION
# ============================================================================

print("\n2. TESTING CONFIGURATION")
print("-" * 70)

def test_config_loading():
    from core.config_manager import get_config
    config = get_config()
    
    # Test getting values
    email_selector = config.get('naukri.email_selector')
    assert email_selector is not None, "Email selector not found"
    
    # Test default config
    all_config = config.get_all()
    assert 'naukri' in all_config, "Naukri config missing"
    assert 'automation' in all_config, "Automation config missing"

test("Configuration loading", test_config_loading)

def test_filter_loading():
    from core.config_manager import get_config
    config = get_config()
    
    filters = config.load_filters()
    assert filters is not None, "Filters not loaded"
    assert 'required_skills' in filters, "Required skills not found"

test("Filter loading", test_filter_loading)

# ============================================================================
# TEST LOGGER
# ============================================================================

print("\n3. TESTING LOGGER")
print("-" * 70)

def test_logger_creation():
    from core.logger import get_logger
    logger = get_logger("test_module")
    assert logger is not None, "Logger not created"

test("Logger creation", test_logger_creation)

def test_logger_output():
    from core.logger import get_logger
    from pathlib import Path
    
    logger = get_logger("test_output")
    logger.info("Test message")
    
    log_file = Path("data/logs/app.log")
    assert log_file.exists(), "Log file not created"

test("Logger output", test_logger_output)

# ============================================================================
# TEST VALIDATORS
# ============================================================================

print("\n4. TESTING VALIDATORS")
print("-" * 70)

def test_email_validation():
    from utils.validators import Validators
    from core.exceptions import ConfigException
    
    # Valid email
    Validators.validate_email("test@example.com")
    
    # Invalid email
    try:
        Validators.validate_email("invalid-email")
        raise AssertionError("Should reject invalid email")
    except ConfigException:
        pass  # Expected

test("Email validation", test_email_validation)

def test_url_validation():
    from utils.validators import Validators
    from core.exceptions import ConfigException
    
    # Valid URL
    Validators.validate_url("https://www.naukri.com")
    
    # Invalid URL
    try:
        Validators.validate_url("not-a-url")
        raise AssertionError("Should reject invalid URL")
    except ConfigException:
        pass  # Expected

test("URL validation", test_url_validation)

def test_experience_validation():
    from utils.validators import Validators
    from core.exceptions import ConfigException
    
    # Valid experience
    Validators.validate_experience(3)
    
    # Invalid experience
    try:
        Validators.validate_experience(-1)
        raise AssertionError("Should reject negative experience")
    except ConfigException:
        pass  # Expected

test("Experience validation", test_experience_validation)

def test_keywords_validation():
    from utils.validators import Validators
    from core.exceptions import ConfigException
    
    # Valid keywords
    Validators.validate_keywords(["Python", "Django"])
    
    # Invalid keywords
    try:
        Validators.validate_keywords([])
        raise AssertionError("Should reject empty keywords")
    except ConfigException:
        pass  # Expected

test("Keywords validation", test_keywords_validation)

# ============================================================================
# TEST HELPERS
# ============================================================================

print("\n5. TESTING HELPERS")
print("-" * 70)

def test_job_id_extraction():
    from utils.helpers import Helpers
    
    url = "https://www.naukri.com/job-listings-python-dev-123456789"
    job_id = Helpers.extract_job_id(url)
    assert job_id is not None, "Job ID not extracted"

test("Job ID extraction", test_job_id_extraction)

def test_filename_sanitization():
    from utils.helpers import Helpers
    
    bad_name = "Invalid<File>Name|*.txt"
    clean = Helpers.sanitize_filename(bad_name)
    assert "<" not in clean, "Special chars not removed"

test("Filename sanitization", test_filename_sanitization)

def test_timestamp():
    from utils.helpers import Helpers
    
    ts = Helpers.get_timestamp()
    assert "T" in ts, "Invalid timestamp format"

test("Timestamp generation", test_timestamp)

def test_duration_formatting():
    from utils.helpers import Helpers
    
    duration = Helpers.format_duration(3665)  # 1h 1m 5s
    assert "h" in duration, "Duration format missing hours"

test("Duration formatting", test_duration_formatting)

def test_json_operations():
    from utils.helpers import Helpers
    import os
    
    # Test save
    test_data = {"key": "value"}
    test_file = "test_temp.json"
    Helpers.save_json(test_data, test_file)
    assert os.path.exists(test_file), "File not saved"
    
    # Test load
    loaded = Helpers.load_json(test_file)
    assert loaded == test_data, "Data not loaded correctly"
    
    # Cleanup
    os.remove(test_file)

test("JSON operations", test_json_operations)

# ============================================================================
# TEST STORAGE
# ============================================================================

print("\n6. TESTING STORAGE")
print("-" * 70)

def test_storage_initialization():
    from modules.storage import StorageModule
    
    storage = StorageModule(storage_type='json')
    assert storage is not None, "Storage not initialized"

test("Storage initialization", test_storage_initialization)

def test_storage_save_apply():
    from modules.storage import StorageModule
    import time
    
    storage = StorageModule(storage_type='json')
    job_id = f"test_job_{int(time.time())}"
    
    success = storage.save_applied_job(
        job_id,
        "Test Job",
        "https://test.com",
        "success"
    )
    assert success, "Job not saved"

test("Storage save", test_storage_save_apply)

def test_storage_duplicate_check():
    from modules.storage import StorageModule
    import time
    
    storage = StorageModule(storage_type='json')
    job_id = f"test_dup_{int(time.time())}"
    
    # Save job
    storage.save_applied_job(job_id, "Test", "https://test.com", "success")
    
    # Check if applied
    is_applied = storage.is_already_applied(job_id)
    assert is_applied, "Duplicate not detected"

test("Storage duplicate check", test_storage_duplicate_check)

def test_storage_statistics():
    from modules.storage import StorageModule
    
    storage = StorageModule(storage_type='json')
    stats = storage.get_statistics()
    assert 'total_applications' in stats, "Stats missing"

test("Storage statistics", test_storage_statistics)

# ============================================================================
# TEST FILTER
# ============================================================================

print("\n7. TESTING FILTER MODULE")
print("-" * 70)

def test_filter_initialization():
    from modules.filter import FilterModule
    
    filter_module = FilterModule()
    assert filter_module is not None, "Filter not initialized"

test("Filter initialization", test_filter_initialization)

def test_filter_job():
    from modules.filter import FilterModule
    
    filter_module = FilterModule()
    test_job = {
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "location": "Bangalore"
    }
    
    user_profile = {
        "skills": ["Python", "Django"],
        "experience": 3
    }
    
    result = filter_module.filter_job(test_job, user_profile)
    assert 'decision' in result, "Decision not made"
    assert 'score' in result, "Score not calculated"

test("Filter job", test_filter_job)

def test_batch_filter():
    from modules.filter import FilterModule
    
    filter_module = FilterModule()
    jobs = [
        {"title": "Python Dev", "company": "Company A"},
        {"title": "Java Dev", "company": "Company B"},
        {"title": "Django Developer", "company": "Company C"}
    ]
    
    user_profile = {"skills": ["Python"], "experience": 2}
    filtered = filter_module.batch_filter(jobs, user_profile)
    assert isinstance(filtered, list), "Filtered result not a list"

test("Batch filter", test_batch_filter)

# ============================================================================
# TEST HUMAN BEHAVIOR
# ============================================================================

print("\n8. TESTING HUMAN BEHAVIOR")
print("-" * 70)

def test_human_behavior_init():
    from utils.human_behavior import HumanBehavior
    
    behavior = HumanBehavior()
    assert behavior is not None, "Behavior not initialized"
    assert behavior.min_delay > 0, "Min delay not set"
    assert behavior.max_delay > 0, "Max delay not set"

test("Human behavior initialization", test_human_behavior_init)

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)
print(f"✓ Passed: {test_results['passed']}")
print(f"✗ Failed: {test_results['failed']}")

if test_results['errors']:
    print("\nFailed Tests:")
    for name, error in test_results['errors']:
        print(f"  - {name}: {error}")

print("\n" + "="*70)

if test_results['failed'] == 0:
    print("✅ ALL TESTS PASSED!")
else:
    print(f"❌ {test_results['failed']} test(s) failed")

print("="*70 + "\n")

sys.exit(0 if test_results['failed'] == 0 else 1)
