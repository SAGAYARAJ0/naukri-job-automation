# Naukri Job Automation System

Automated job application system for Naukri platform using Python and Selenium.

## Features

- ✅ Automated login with CAPTCHA handling
- ✅ Job search with filters (keywords, location, experience)
- ✅ Intelligent job filtering based on skills and experience
- ✅ Automatic job application
- ✅ Duplicate prevention with persistent storage
- ✅ Human behavior simulation (delays, scrolling, realistic clicks)
- ✅ Comprehensive logging and error handling
- ✅ Configuration-driven approach
- ✅ Scheduled execution support

## Project Structure

```
python-job-automation/
├── config/
│   ├── config.json              # Main configuration
│   ├── filters.json             # Job filter rules
│   └── config_template.json     # Template for setup
├── modules/
│   ├── login.py                 # Authentication module
│   ├── search.py                # Job search module
│   ├── filter.py                # Job filtering module
│   ├── apply.py                 # Application module
│   ├── storage.py               # Data persistence
│   └── scheduler.py             # Scheduled execution
├── core/
│   ├── exceptions.py            # Custom exceptions
│   ├── logger.py                # Logging system
│   ├── config_manager.py        # Config management
│   └── driver_manager.py        # Selenium driver
├── utils/
│   ├── human_behavior.py        # Human simulation
│   ├── validators.py            # Input validators
│   └── helpers.py               # Helper utilities
├── data/
│   ├── logs/                    # Log files
│   └── applied_jobs.json        # Job history
├── main.py                      # Main orchestrator
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

```bash
# Clone repository
cd python-job-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download ChromeDriver (automatic with webdriver-manager)
```

## Configuration

1. **Edit `config/config.json`:**
   ```json
   {
       "credentials": {
           "email": "your-email@naukri.com",
           "password": "your-password"
       },
       "automation": {
           "headless": false,
           "implicit_wait": 10
       }
   }
   ```

2. **Edit `config/filters.json`:**
   ```json
   {
       "required_skills": ["Python", "JavaScript", "SQL"],
       "preferred_locations": ["Bangalore", "Mumbai"],
       "filter_threshold": 70
   }
   ```

## Usage

### Run Once
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

### Schedule Daily
```python
orchestrator.schedule_automation(
    email="your@email.com",
    password="your-password",
    keywords=["Python", "Backend"],
    location="Bangalore",
    experience=3,
    schedule_type='daily',
    start_hour=9  # Run at 9 AM
)
```

### Schedule Every N Hours
```python
orchestrator.schedule_automation(
    email="your@email.com",
    password="your-password",
    keywords=["Python", "Backend"],
    location="Bangalore",
    experience=3,
    schedule_type='interval',
    hours=12  # Run every 12 hours
)
```

## Module Details

### Login Module (`modules/login.py`)
- Handles Naukri authentication
- Automatic CAPTCHA detection and pause
- Session cookie management
- Fallback to saved sessions

### Search Module (`modules/search.py`)
- Builds dynamic search URLs
- Handles pagination
- Extracts job listings with metadata
- Human-like scrolling and delays

### Filter Module (`modules/filter.py`)
- NLP-based skill matching
- Experience requirement checking
- Red flag detection
- Scoring-based decision making

### Apply Module (`modules/apply.py`)
- Finds and clicks apply buttons
- Handles external redirects
- Verifies application success
- Retry mechanism with backoff

### Storage Module (`modules/storage.py`)
- JSON or SQLite storage options
- Duplicate prevention
- Statistics tracking
- Export capabilities

### Scheduler Module (`modules/scheduler.py`)
- APScheduler integration
- Interval, cron, and daily scheduling
- Execution history tracking
- Pause/resume functionality

## Logging

Logs are stored in `data/logs/`:
- `app.log` - Main application log
- `error.log` - Error-specific logs
- `debug.log` - Debug-level information

## Error Handling

The system handles:
- Network timeouts with exponential backoff
- Stale element references with re-tries
- Rate limiting (429 errors)
- Session expiration
- CAPTCHA detection and pausing

## Human Behavior Features

To avoid detection:
- Random delays (2-5 seconds)
- Realistic typing speed (character-by-character)
- Human-like scrolling patterns
- Mouse movement with offsets
- Random page exploration

## Security

- ⚠️ **Never commit `config/config.json` with credentials**
- Add to `.gitignore`: `config/config.json`
- Store credentials in environment variables for production
- Use HTTPS only
- Rotate cookies periodically

## Troubleshooting

### CAPTCHA not solving automatically
- The system pauses for 300 seconds for manual solving
- Solve CAPTCHA in the browser and the system continues automatically

### Login fails
- Verify credentials in `config/config.json`
- Check if UI selectors have changed (update in config)
- Check logs in `data/logs/app.log`

### No jobs found
- Verify keywords in search
- Check filter criteria in `config/filters.json`
- Reduce filter threshold for more results

### Rate limiting
- System uses exponential backoff automatically
- Wait between retries increases exponentially
- Consider scheduling during off-peak hours

## Best Practices

1. **Start slowly**: Run with `headless=false` to monitor behavior
2. **Monitor logs**: Check `data/logs/app.log` for issues
3. **Test filters**: Run searches before full automation
4. **Adjust delays**: Increase `min_delay`/`max_delay` if rate limited
5. **Regular breaks**: Schedule runs with suitable intervals
6. **Backup history**: Export `applied_jobs.json` regularly

## Performance Tips

- Use `headless: true` for faster execution
- Reduce `max_pages` for quicker searches
- Lower `filter_threshold` for fewer applications
- Increase delays if getting rate limited
- Batch applications during off-peak hours

## Limitations

- CAPTCHA must be solved manually (pause mode)
- Naukri UI changes may break selectors
- Rate limiting by Naukri applies
- No direct API access (browser automation only)

## Contributing

Improvements welcome! Areas to enhance:
- Better NLP for job matching
- Email notifications
- Browser profile management
- Multi-account support

## License

MIT License - Use freely with attribution

## Disclaimer

This tool is for educational purposes. Use responsibly and follow Naukri's Terms of Service. Not liable for account bans or rate limiting.

## Support

For issues:
1. Check logs in `data/logs/`
2. Verify configuration
3. Update selectors if UI changed
4. Review error messages

---

**Last Updated**: April 2026
**Version**: 1.0.0
