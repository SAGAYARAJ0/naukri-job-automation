"""
Quick Reference Guide - Naukri Job Automation
One-page cheat sheet for common tasks
"""

# 🚀 QUICK REFERENCE GUIDE

## File Locations

```
Key Files:
├── config/config.json          👈 Edit credentials here
├── config/filters.json         👈 Edit job filters here
├── main.py                     👈 Main entry point
├── example_usage.py            👈 Usage examples
├── run_scheduled.py            👈 Scheduled runner
├── data/logs/app.log           👈 Check logs here
├── data/applied_jobs.json      👈 Application history
└── SETUP_GUIDE.md              👈 Installation guide
```

## Configuration Quick Setup

### 1. Update Credentials
```json
// config/config.json
{
    "credentials": {
        "email": "your-email@naukri.com",
        "password": "your-password"
    }
}
```

### 2. Update Search Criteria
```json
// config/filters.json
{
    "required_skills": ["Python", "Django"],
    "preferred_locations": ["Bangalore"],
    "min_experience": 2,
    "filter_threshold": 70
}
```

### 3. Adjust Automation Speed
```json
// config/config.json
{
    "behavior": {
        "min_delay": 2,      // Minimum seconds between actions
        "max_delay": 5       // Maximum seconds between actions
    }
}
```

## Quick Commands

```bash
# Install
cd "e:\python job automation"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run once
python main.py

# Run with examples
python example_usage.py

# Schedule daily (9 AM)
python run_scheduled.py --schedule

# View logs
Get-Content -Path "data/logs/app.log" -Tail 50

# Check history
python -c "from modules import get_storage_module; s=get_storage_module(); print(f'Total: {s.get_application_count()}')"

# Export history
python -c "from modules import get_storage_module; get_storage_module().export_history()"
```

## Python API Quick Start

### Single Run
```python
from main import Orchestrator

orch = Orchestrator()
orch.run_automation(
    email="user@naukri.com",
    password="password",
    keywords=["Python", "Backend"],
    location="Bangalore",
    experience=3
)
```

### Schedule Daily
```python
orch.schedule_automation(
    email="user@naukri.com",
    password="password",
    keywords=["Python", "Backend"],
    location="Bangalore",
    experience=3,
    schedule_type='daily',
    start_hour=9  # 9 AM
)
```

### Check Statistics
```python
from modules import get_storage_module

storage = get_storage_module()
print(f"Total applications: {storage.get_application_count()}")
print(f"Statistics: {storage.get_statistics()}")
```

## Common Issues & Fixes

### Issue: Login fails
```
🔍 Check:
- Is email/password correct?
- Add to config/config.json
- Check logs: data/logs/error.log
```

### Issue: CAPTCHA appears
```
⏸️ System pauses for solving
- Solve CAPTCHA in browser window
- System continues after 5 minutes or CAPTCHA solved
```

### Issue: No jobs applied
```
📊 Check:
- Are jobs matching filter criteria?
- Lower filter_threshold in config
- Check logs for filter results
```

### Issue: Getting rate limited
```
🛑 Solution:
1. Increase delays in config
2. Run less frequently
3. Run during off-peak hours
```

### Issue: UI elements not found
```
🔧 Solution:
1. UI may have changed
2. Update selectors in config/config.json
3. Inspect Naukri website with DevTools
4. Find new selector values
```

## Environment Variables (Production)

```bash
# Set instead of hardcoding in config
export NAUKRI_EMAIL="your@email.com"
export NAUKRI_PASSWORD="your-password"
export NAUKRI_KEYWORDS="Python,Django"
export NAUKRI_LOCATION="Bangalore"
export NAUKRI_EXPERIENCE="3"

# Export in Python
import os
email = os.getenv('NAUKRI_EMAIL')
```

## Logging Levels

Files in `data/logs/`:
- **app.log** - General info + debug + errors
- **error.log** - Errors and warnings only
- **debug.log** - Detailed debug messages

```bash
# View in real-time
Get-Content -Path "data/logs/app.log" -Tail 50 -Wait

# Search for errors
Select-String "ERROR" "data/logs/error.log"

# Count applications
Select-String "successfully applied" "data/logs/app.log" | Measure-Object
```

## Troubleshooting Flowchart

```
Problem?
├─ Login fails?
│  ├─ Check credentials ✓
│  ├─ Check 2FA ✓
│  └─ Update selectors in config ✓
│
├─ No jobs found?
│  ├─ Check keywords ✓
│  ├─ Check location ✓
│  └─ Lower filter_threshold ✓
│
├─ Rate limited?
│  ├─ Increase delays in config ✓
│  ├─ Run less frequently ✓
│  └─ Run during off-peak hours ✓
│
├─ Elements not found?
│  ├─ Update selectors in config ✓
│  ├─ Restart automation ✓
│  └─ Check if UI changed ✓
│
└─ Other issues?
   └─ Check data/logs/error.log ✓
```

## Performance Tuning

### Faster Execution
```json
{
    "headless": true,
    "max_pages": 5,
    "behavior": {
        "min_delay": 1,
        "max_delay": 2
    }
}
```

### Safer Execution
```json
{
    "headless": false,
    "max_pages": 20,
    "behavior": {
        "min_delay": 5,
        "max_delay": 10
    }
}
```

### Balanced
```json
{
    "headless": false,
    "max_pages": 10,
    "behavior": {
        "min_delay": 2,
        "max_delay": 5
    }
}
```

## File Structure Reminder

```
data/
├── logs/
│   ├── app.log      ← Main log
│   ├── error.log    ← Errors only
│   └── debug.log    ← Debug details
├── applied_jobs.json ← History (JSON)
└── jobs.db          ← History (SQLite - if enabled)

config/
├── config.json      ← Main config
└── filters.json     ← Filter rules

modules/
├── login.py         ← Login logic
├── search.py        ← Search logic
├── filter.py        ← Filter logic
├── apply.py         ← Apply logic
├── storage.py       ← Storage logic
└── scheduler.py     ← Scheduling
```

## Status Meanings

| Status | Meaning |
|--------|---------|
| ✓ success | Job applied successfully |
| ⊗ already_applied | Already applied to this job |
| ✗ failed | Application failed |
| 🔗 external | Redirect to external site |
| ⏸️ captcha_required | CAPTCHA needed |

## Key Metrics to Monitor

```
Track these in statistics:
├─ Total applications
├─ Success rate
├─ Filter rate
├─ Duplicate skipped
└─ Error count
```

## When to Check Logs

✅ After each run
✅ If jobs not applied
✅ If filters not working
✅ If errors occur
✅ For performance analysis

## Backup Important Files

```bash
# Backup job history periodically
copy data\applied_jobs.json data\backup_$(date /+%Y%m%d).json

# Backup config
copy config\config.json config\config_backup.json
```

## Emergency Stop

```bash
# Stop scheduled automation
Ctrl + C  (in terminal running scheduler)

# Or kill process
Get-Process python | Stop-Process

# Clean up
taskkill /F /IM python.exe
```

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Update credentials: Edit `config/config.json`
3. ✅ Test run: `python example_usage.py`
4. ✅ Monitor logs: `data/logs/app.log`
5. ✅ Schedule: `python run_scheduled.py --schedule`

---

**Remember**: Always check logs for detailed information!

**Log Location**: `data/logs/app.log`

**Need Help?** 
- Check `SETUP_GUIDE.md` for installation
- Check `README.md` for full documentation
- Review logs for specific errors
