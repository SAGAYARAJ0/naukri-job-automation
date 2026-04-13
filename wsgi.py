"""
WSGI entrypoint for Naukri Job Automation
Used by production servers like Gunicorn and Vercel
"""

from app import app

if __name__ == "__main__":
    app.run()
