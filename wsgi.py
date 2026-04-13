"""
WSGI entrypoint for Naukri Job Automation
Used by production servers like Gunicorn, uWSGI, Heroku, etc.
"""

from app import app

if __name__ == "__main__":
    app.run()
