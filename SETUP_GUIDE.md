"""
Setup and Installation Guide for Naukri Job Automation System
"""

# SETUP GUIDE

## Step 1: Prerequisites

```bash
# Verify Python 3.8+
python --version

# Verify pip
pip --version
```

## Step 2: Installation

```bash
# Navigate to project directory
cd "e:\python job automation"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# WebDriver will be auto-downloaded on first run
```

## Step 3: Configuration

### 3A. Update Credentials

Edit `config/config.json`:

```json
{
    "credentials": {
        "email": "your-actual-email@naukri.com",
        "password": "your-actual-password"
    },
    ...
}
```

⚠️ **IMPORTANT**: Add to `.gitignore` to prevent credential leaks:
```
config/config.json
```

### 3B. Customize Job Filters

Edit `config/filters.json`:

```json
{
    "required_skills": ["Python", "Django", "REST API"],
    "nice_to_have_skills": ["Docker", "PostgreSQL", "AWS"],
    "red_flags": ["unpaid", "internship only", "contract"],
    "min_experience": 2,
    "preferred_locations": ["Bangalore", "Remote"],
    "preferred_salary_range": [800000, 2500000],
    "filter_threshold": 75
}
```

### 3C. Adjust Automation Settings

Edit `config/config.json` automation section:

```json
{
    "automation": {
        "headless": false,          # false = see browser, true = hidden
        "implicit_wait": 10,        # seconds
        "explicit_wait": 15,        # seconds
        "page_load_timeout": 20,    # seconds
        "captcha_timeout": 300,     # 5 minutes for manual CAPTCHA
        "max_retries": 3,           # retry attempts
        "backoff_factor": 2         # exponential backoff
    },
    "behavior": {
        "min_delay": 2,             # seconds between actions
        "max_delay": 5,             # seconds between actions
        "typing_speed": 0.1,        # seconds per character
        "scroll_pause": 3,          # pause after scroll
        "scroll_amount": 3          # scroll distance
    }
}
```

## Step 4: Test Installation

```bash
# Run with example usage menu
python example_usage.py

# Or run basic automation test
python main.py
```

## Step 5: Run the System

### Option A: Single Run

```python
from main import Orchestrator

orchestrator = Orchestrator()
orchestrator.run_automation(
    email="your@email.com",
    password="your-password",
    keywords=["Python", "Backend"],
    location="Bangalore",
    experience=3
)
```

### Option B: Daily Schedule (9 AM)

```bash
python run_scheduled.py --schedule
```

Keep the terminal open. The script will run every day at 9 AM.

### Option C: Use Example Menu

```bash
python example_usage.py

# Choose option from menu
```

## Step 6: Monitor Execution

### View Logs

```bash
# Real-time logs (on Windows)
Get-Content -Path "data/logs/app.log" -Tail 20 -Wait

# Or view file directly
code data/logs/app.log
```

### Check Application History

```bash
# View applied_jobs.json
python -c "import json; print(json.dumps(json.load(open('data/applied_jobs.json')), indent=2))"
```

### Export History

```python
from modules import get_storage_module

storage = get_storage_module()
stats = storage.get_statistics()
print(stats)

# Export to file
storage.export_history()
```

## Step 7: Troubleshooting

### Issue: CAPTCHA appears but doesn't auto-solve

**Solution**: System pauses for 300 seconds (5 minutes). Solve CAPTCHA manually in the browser window, then it continues automatically.

### Issue: Login fails

**Checklist**:
- [ ] Credentials are correct in `config/config.json`
- [ ] Account doesn't have 2FA enabled (or disable temporarily)
- [ ] No IP blocks from Naukri
- [ ] Browser opens successfully

**Debug**:
```bash
# Run with headless: false to see browser
# Check logs: data/logs/error.log
```

### Issue: No jobs found

**Checklist**:
- [ ] Keywords exist on Naukri
- [ ] Location is valid
- [ ] Filter threshold is not too high

**Solution**:
```json
{
    "filter": {
        "threshold": 60  // Lower from 70
    }
}
```

### Issue: Getting rate limited (429 errors)

**Solution**:
- Increase delays in config:
  ```json
  {
      "behavior": {
          "min_delay": 5,
          "max_delay": 10
      }
  }
  ```
- Schedule runs during off-peak hours
- Run less frequently

### Issue: UI selectors changed (ElementNotFound)

**Solution**: Update selectors in `config/config.json`:

```bash
# Inspect Naukri website with browser DevTools
# Find new selector for each element:
# - Email field
# - Password field
# - Login button

# Update in config
{
    "naukri": {
        "email_selector": "new-selector",
        ...
    }
}
```

## Step 8: Production Deployment

### Option A: Windows Task Scheduler

```powershell
# Create task that runs hourly
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Hours 1) -At "09:00" -RepetitionDuration (New-TimeSpan -Days 365)

$action = New-ScheduledTaskAction -Execute "python" -Argument "main.py" -WorkingDirectory "e:\python job automation"

Register-ScheduledTask -TaskName "NaukriAutomation" -Trigger $trigger -Action $action -RunLevel Highest
```

### Option B: Linux/Mac with Cron

```bash
# Edit crontab
crontab -e

# Add entry (daily at 9 AM):
0 9 * * * cd /path/to/automation && /path/to/venv/bin/python main.py

# Or every 12 hours:
0 */12 * * * cd /path/to/automation && /path/to/venv/bin/python main.py
```

### Option C: Docker (Advanced)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y chromium-browser
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```

## Step 9: Best Practices

### Security
- ✅ Store credentials in environment variables (production)
- ✅ Add `config/config.json` to `.gitignore`
- ✅ Use HTTPS only
- ✅ Rotate cookies periodically

### Performance
- ✅ Use `headless: true` for faster execution
- ✅ Reduce `max_pages` for quicker searches
- ✅ Lower `filter_threshold` if getting rate limited
- ✅ Schedule during off-peak hours

### Monitoring
- ✅ Check logs regularly
- ✅ Monitor success rate
- ✅ Export history weekly
- ✅ Set up email/SMS alerts (future enhancement)

### Maintenance
- ✅ Update Selenium monthly
- ✅ Monitor for UI changes on Naukri
- ✅ Test filters regularly
- ✅ Back up `applied_jobs.json`

## Step 10: Troubleshooting Commands

```bash
# Check Python install
python --version

# Check pip packages
pip list

# Verify Selenium
python -c "from selenium import webdriver; print('✓ Selenium OK')"

# Test WebDriver
python -c "from selenium.webdriver.chrome.service import Service; from selenium import webdriver; print('✓ ChromeDriver OK')"

# Check logs
tail -f data/logs/app.log

# Run with debug logging
python main.py --debug

# Test config load
python -c "from core import get_config; print(get_config().get_all())"
```

## Support & Issues

**Common Issues & Solutions**:
1. **ChromeDriver not found** → Run `pip install webdriver-manager` 
2. **Import errors** → Run `pip install -r requirements.txt`
3. **Permission denied** → Check folder permissions
4. **Port conflicts** → Change scheduler port in config

**Debug Mode**:
```bash
# Enable debug logging
PYTHONUNBUFFERED=1 python main.py
```

**Get help**:
- Check `data/logs/error.log`
- Review error messages carefully
- Check README.md for more details
- Update selectors if UI changed

---

## Quick Start Summary

```bash
# 1. Setup
cd "e:\python job automation"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure
# Edit config/config.json with your credentials

# 3. Test
python example_usage.py

# 4. Run
python main.py

# 5. Schedule (optional)
python run_scheduled.py --schedule
```

**That's it!** The automation system is ready to use.

---

**Version**: 1.0.0  
**Last Updated**: April 2026  
**Status**: Production Ready ✓
