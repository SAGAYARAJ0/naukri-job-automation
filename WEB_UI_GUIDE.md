# 🎨 Web UI for Naukri Job Automation

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials
Edit `.env` file:
```
NAUKRI_EMAIL=your-email@gmail.com
NAUKRI_PASSWORD=your-password
```

### 3. Run the Web Server
```bash
python app.py
```

### 4. Open in Browser
Go to: **http://localhost:5000**

---

## 🎯 Features

### Search & Filter
- **Job Title/Skills**: Search for specific roles (Java Developer, Spring Boot, Python, etc.)
- **Experience Level**: Select your years of experience (Fresher to 10+ Years)
- **Location**: Enter preferred location (Bangalore, Delhi, Mumbai, etc.)
- **Freshness**: Filter by posting date (Last 1/3/7/15/30 days)

### Real-time Statistics
- **Total Applications**: See how many jobs you've applied to
- **Success Rate**: Track application success percentage
- **System Status**: Check if credentials are configured

### Application History
- View all applications
- See status of each application
- Direct links to job postings
- Application timestamps

---

## 📱 Interface Components

### Search Section (Left Panel)
```
┌─────────────────────────────────┐
│  🔍 Search Jobs                 │
├─────────────────────────────────┤
│  Job Title / Skills             │
│  [Java Developer, Spring Boot...│
│                                 │
│  Experience      │  Location    │
│  [3 Years    ]   │  [Bangalore] │
│                                 │
│  📅 Posted Within               │
│  [1][3][7][15][30] days        │
│                                 │
│  [🚀 Search & Apply]            │
└─────────────────────────────────┘
```

### Statistics Panel (Right Panel)
```
┌─────────────────────────────────┐
│  📊 Statistics                  │
├─────────────────────────────────┤
│  Total Applications             │
│  42                             │
│                                 │
│  Success Rate                   │
│  78.5%                          │
│                                 │
│  System Status                  │
│  ✓ Ready                        │
└─────────────────────────────────┘
```

### Recent Applications (Full Width)
```
┌──────────────────────────────────────┐
│  📝 Recent Applications              │
├──────────────────────────────────────┤
│  Java Developer at TechCorp          │
│  Bangalore  [✓ Applied] Apr 13, 2026 │
│                                      │
│  Spring Boot Dev at Infosys          │
│  Delhi [✓ Applied] Apr 12, 2026      │
│                                      │
│  Python Developer at Google          │
│  Bangalore [⏳ Pending] Apr 10, 2026 │
└──────────────────────────────────────┘
```

---

## 🔌 API Endpoints

### `POST /api/search`
Search and apply to jobs
```json
Request:
{
  "keywords": "Java Developer, Spring Boot",
  "experience": "3",
  "location": "Bangalore",
  "freshness": "7"
}

Response:
{
  "success": true,
  "message": "Search completed",
  "credentials_masked": "ssagayaraj***@****"
}
```

### `GET /api/jobs`
Get saved applications
```json
Response:
{
  "success": true,
  "jobs": [
    {
      "title": "Java Developer",
      "company": "TechCorp",
      "location": "Bangalore",
      "status": "success",
      "applied_at": "2026-04-13T13:28:15"
    }
  ],
  "total": 42
}
```

### `GET /api/stats`
Get statistics
```json
Response:
{
  "success": true,
  "total_applications": 42,
  "successful": 33,
  "success_rate": 78.5
}
```

### `GET /api/health`
System health check
```json
Response:
{
  "status": "healthy",
  "credentials_configured": true,
  "data_directory_exists": true,
  "logs_exist": true
}
```

---

## 🎨 Design Features

- **Modern Gradient UI**: Purple gradient background
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Auto-refresh stats every 30 seconds
- **Status Indicators**: Visual badges for application status
- **Loading States**: Clear feedback during operations
- **Error Handling**: User-friendly error messages

---

## 📊 Supported Job Filters

### Skills/Titles
- Java Developer
- Spring Boot Developer
- Python Developer
- React Developer
- Node.js Developer
- Full Stack Developer
- Data Scientist
- And many more...

### Experience Levels
- Fresher (0 years)
- 1 Year
- 2 Years
- 3 Years
- 5 Years
- 7 Years
- 10+ Years

### Locations
- Bangalore
- Delhi
- Mumbai
- Hyderabad
- Pune
- Chennai
- And more...

### Freshness
- Last 1 day
- Last 3 days
- Last 7 days
- Last 15 days
- Last 30 days

---

## 🐛 Troubleshooting

### "Credentials not configured"
Check `.env` file:
```bash
cat .env
# Should show:
# NAUKRI_EMAIL=your-email@gmail.com
# NAUKRI_PASSWORD=your-password
```

### "Port 5000 already in use"
Use a different port:
```bash
python -c "from app import app; app.run(port=8000)"
```

### "Module not found: flask"
Install missing dependency:
```bash
pip install flask==2.3.3
```

### Search not returning results
- Check internet connection
- Verify Naukri credentials
- Check browser console (F12) for errors
- View logs in `data/logs/app.log`

---

## 📝 Log Files

All operations are logged to:
- `data/logs/app.log` - General logs
- `data/logs/error.log` - Error logs
- `data/logs/debug.log` - Debug logs

View real-time logs:
```bash
# Windows
tail -f data/logs/app.log

# Or in Python
python -c "
import time
with open('data/logs/app.log') as f:
    while True:
        print(f.readline(), end='')
        time.sleep(0.1)
"
```

---

## 🚀 Advanced Usage

### Custom Port
```bash
python -c "from app import app; app.run(port=8080)"
```

### Public Access (not recommended)
```bash
python -c "from app import app; app.run(host='0.0.0.0')"
```

### Production Deployment
Use Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📧 Support

For issues:
1. Check `data/logs/app.log`
2. Review `.env` configuration
3. Verify Naukri credentials
4. Check internet connection

---

**Created**: April 13, 2026
**Version**: 1.0.0
**Status**: ✅ Production Ready
