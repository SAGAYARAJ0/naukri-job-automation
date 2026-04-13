# 🚀 Deployment Guide - Naukri Job Automation

## Quick Start - Cloud Deployment

Your project is configured for easy deployment to multiple cloud platforms.

---

## 📋 Prerequisites

- Git installed and initialized (✓ Already done)
- GitHub repository created (✓ Already done)
- Requirements.txt with all dependencies (✓ Already done)
- .env file with credentials (✓ Already done)
- Procfile for Heroku (✓ Already done)
- pyproject.toml for packaging (✓ Already done)
- wsgi.py entrypoint (✓ Already done)

---

## 🌐 Deployment Options

### Option 1: Heroku (Most Popular - FREE TIER AVAILABLE)

**Step 1: Install Heroku CLI**
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or use Chocolatey on Windows:
choco install heroku-cli
```

**Step 2: Login to Heroku**
```bash
heroku login
```

**Step 3: Create Heroku App**
```bash
cd "e:\python job automation"
heroku create naukri-job-automation
```

**Step 4: Set Environment Variables**
```bash
heroku config:set NAUKRI_EMAIL=your-email@gmail.com
heroku config:set NAUKRI_PASSWORD=your-password
```

**Step 5: Deploy**
```bash
git push heroku main
```

**Step 6: View Logs**
```bash
heroku logs --tail
```

**Access Your App**
```
https://naukri-job-automation.herokuapp.com
```

---

### Option 2: Railway.app (Simple & Affordable)

**Step 1: Create Account**
- Go to https://railway.app
- Sign in with GitHub

**Step 2: Create New Project**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your naukri-job-automation repo

**Step 3: Add Environment Variables**
- In Railway dashboard: Variables
- Add:
  ```
  NAUKRI_EMAIL=your-email@gmail.com
  NAUKRI_PASSWORD=your-password
  FLASK_ENV=production
  ```

**Step 4: Deploy**
- Railway auto-deploys on push!
- Check deployment status in dashboard

---

### Option 3: PythonAnywhere (Python-Specific)

**Step 1: Create Account**
- Go to https://www.pythonanywhere.com
- Create free account

**Step 2: Clone Repository**
```bash
# In PythonAnywhere console:
git clone https://github.com/SAGAYARAJ0/naukri-job-automation.git
cd naukri-job-automation
pip install -r requirements.txt
```

**Step 3: Create Web App**
- Web -> Add new web app
- Choose "Flask"
- Python 3.11
- Use WSGI configuration

**Step 4: Configure WSGI**
- Edit WSGI file: `/var/www/<username>_pythonanywhere_com_wsgi.py`
- Replace with:
```python
import sys
path = '/home/<username>/naukri-job-automation'
sys.path.append(path)

from wsgi import app
application = app
```

**Step 5: Set Environment Variables**
- Web -> Environment variables
- Add NAUKRI_EMAIL and NAUKRI_PASSWORD

**Step 6: Reload App**
- Click "Reload" green button

---

### Option 4: Docker (For Any Host)

**Step 1: Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=wsgi:app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

**Step 2: Build & Test Locally**
```bash
docker build -t naukri-automation .
docker run -p 5000:5000 -e NAUKRI_EMAIL=your-email -e NAUKRI_PASSWORD=your-password naukri-automation
```

**Step 3: Deploy to Any Docker-Enabled Host**
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

---

### Option 5: AWS Elastic Beanstalk

**Step 1: Install EB CLI**
```bash
pip install awsebcli
```

**Step 2: Initialize**
```bash
cd "e:\python job automation"
eb init -p python-3.11 naukri-automation
eb create naukri-automation-env
```

**Step 3: Configure Environment**
```bash
eb setenv NAUKRI_EMAIL=your-email@gmail.com
eb setenv NAUKRI_PASSWORD=your-password
```

**Step 4: Deploy**
```bash
eb deploy
```

**Step 5: Open App**
```bash
eb open
```

---

## ⚙️ Configuration Files Explained

### `Procfile`
- Tells hosting platform how to start your app
- Runs: `gunicorn wsgi:app`
- Uses `wsgi.py` as entrypoint

### `runtime.txt`
- Specifies Python version (3.11.8)
- Ensures compatibility

### `wsgi.py`
- WSGI application entrypoint
- Used by production servers
- Imports Flask app from app.py

### `pyproject.toml`
- Modern Python packaging configuration
- Specifies dependencies
- Project metadata
- Build system requirements

### `requirements.txt`
- List of all Python packages
- Versions pinned for reproducibility
- Includes gunicorn for production

---

## 🔐 Security Checklist

Before deploying:

- ✅ `.env` file is in `.gitignore` (never committed)
- ✅ Credentials set as environment variables (not in code)
- ✅ HTTPS enabled (automatic on Heroku, Railway, etc.)
- ✅ Debug mode OFF in production (check app.py)
- ✅ No hardcoded secrets in any file
- ✅ Dependencies up-to-date in requirements.txt

---

## 🚨 Common Deployment Issues

### "No module named 'app'"
**Solution**: Ensure `app.py` is in root directory and `wsgi.py` imports it correctly

### "ModuleNotFoundError: No module named 'flask'"
**Solution**: 
```bash
pip install -r requirements.txt
```

### "Port already in use"
**Solution**: Platform assigns port automatically, don't hardcode 5000

### "Credentials not found"
**Solution**: Set environment variables in platform dashboard
```bash
NAUKRI_EMAIL=your-email@gmail.com
NAUKRI_PASSWORD=your-password
```

### "Application not starting"
**Solution**: Check logs
```bash
heroku logs --tail          # Heroku
railway logs                # Railway
```

---

## 📊 Recommended Deployment

| Platform | Cost | Ease | Performance | Recommendation |
|----------|------|------|-------------|---|
| **Heroku** | Free/Paid | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | **Best for beginners** |
| **Railway** | $5-20/mo | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Best value** |
| **PythonAnywhere** | Free/Paid | ⭐⭐⭐⭐ | ⭐⭐⭐ | **Python-specific** |
| **AWS EB** | Paid | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Enterprise** |
| **Docker** | Varies | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **Maximum control** |

**Recommendation**: Start with **Heroku** or **Railway** for simplicity!

---

## 📈 Monitoring After Deployment

### View Logs
```bash
# Heroku
heroku logs --tail

# Railway (in dashboard)
```

### Monitor Performance
- Check response times
- Review error logs
- Monitor API endpoints

### Update Code
```bash
# Make changes locally
git add .
git commit -m "Fix: ..."

# Deploy to Heroku
git push heroku main

# Or Railway (auto-deploys from GitHub)
```

---

## 🔄 Local Testing Before Deploy

Always test locally first:

```bash
# Install dependencies
pip install -r requirements.txt

# Run web server
python run_web_ui.py

# Or run with gunicorn (like production)
gunicorn wsgi:app --bind 0.0.0.0:5000

# Test API endpoints
curl http://localhost:5000/api/health
```

---

## 🎯 Next Steps

1. **Choose a platform** (Heroku or Railway recommended)
2. **Create account** and follow platform-specific setup
3. **Set environment variables** (NAUKRI_EMAIL, NAUKRI_PASSWORD)
4. **Deploy**: Push code or connect GitHub repo
5. **Access**: Visit your app URL
6. **Test**: Use search form on web UI
7. **Monitor**: Check logs for errors

---

## 📞 Support

If deployment fails:

1. Check platform logs
2. Verify `.env` is NOT committed
3. Verify environment variables are set correctly
4. Test locally first: `python run_web_ui.py`
5. Check `requirements.txt` has all dependencies

---

## 📚 Useful Links

- **Heroku**: https://devcenter.heroku.com
- **Railway**: https://docs.railway.app
- **PythonAnywhere**: https://help.pythonanywhere.com
- **AWS Beanstalk**: https://docs.aws.amazon.com/elasticbeanstalk
- **Gunicorn**: https://gunicorn.org

---

## ✅ Deployment Checklist

- [ ] Clone code locally and test: `python run_web_ui.py`
- [ ] Verify `.env` file exists with credentials
- [ ] Verify all dependencies in `requirements.txt`
- [ ] Create account on chosen platform
- [ ] Set environment variables on platform
- [ ] Deploy (push to Heroku/Railway or upload)
- [ ] Check platform logs for errors
- [ ] Access webapp URL
- [ ] Test search functionality
- [ ] Monitor logs for 24 hours

---

**Version**: 1.0.0
**Last Updated**: April 13, 2026
**Status**: ✅ Ready for Production
