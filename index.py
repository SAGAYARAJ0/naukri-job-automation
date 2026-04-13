"""
API Routes for Vercel
This file exports the Flask app as 'app' for Vercel to find
"""

from app import app

# Vercel looks for an 'app' variable in:
# app.py, index.py, server.py, wsgi.py, asgi.py, main.py
# This file ensures Vercel can find our Flask application

__all__ = ['app']
