"""
Web interface for Naukri Job Automation System
Flask-based UI for searching and applying to jobs
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from main import Orchestrator
from core import get_logger
from utils.helpers import get_helpers

app = Flask(__name__)
logger = get_logger(__name__)
helpers = get_helpers()

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@app.route('/')
def index():
    """Home page with search form"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search_jobs():
    """API endpoint for job search"""
    try:
        data = request.json
        
        keywords = data.get('keywords', ['Python']).split(',')
        keywords = [k.strip() for k in keywords if k.strip()]
        
        location = data.get('location', 'Bangalore')
        experience = int(data.get('experience', 3))
        freshness = data.get('freshness', '7')  # days
        
        logger.info(f"Search request: {keywords}, {location}, {experience}yrs, within {freshness} days")
        
        # Initialize orchestrator
        orchestrator = Orchestrator()
        
        # Get credentials from environment
        email = os.getenv('NAUKRI_EMAIL')
        password = os.getenv('NAUKRI_PASSWORD')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Credentials not configured. Please set NAUKRI_EMAIL and NAUKRI_PASSWORD in .env file'
            }), 400
        
        # Run automation
        success = orchestrator.run_automation(
            email, 
            password, 
            keywords, 
            location, 
            experience,
            max_pages=2
        )
        
        return jsonify({
            'success': True,
            'message': 'Search completed',
            'credentials_masked': f"{email[:10]}***@****"
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get saved jobs from storage"""
    try:
        applied_jobs = helpers.load_json('data/applied_jobs.json')
        
        if not applied_jobs:
            return jsonify({
                'success': True,
                'jobs': [],
                'total': 0
            })
        
        # Convert to list if dict
        if isinstance(applied_jobs, dict):
            jobs_list = list(applied_jobs.values())
        else:
            jobs_list = applied_jobs
        
        return jsonify({
            'success': True,
            'jobs': jobs_list[:50],  # Last 50 jobs
            'total': len(jobs_list)
        })
        
    except Exception as e:
        logger.error(f"Error loading jobs: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'jobs': [],
            'total': 0
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get automation statistics"""
    try:
        applied_jobs = helpers.load_json('data/applied_jobs.json')
        
        total = len(applied_jobs) if applied_jobs else 0
        successful = len([j for j in (applied_jobs.values() if isinstance(applied_jobs, dict) else applied_jobs) 
                         if j.get('status') == 'success']) if applied_jobs else 0
        
        return jsonify({
            'success': True,
            'total_applications': total,
            'successful': successful,
            'success_rate': (successful / total * 100) if total > 0 else 0
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            'success': False,
            'total_applications': 0,
            'successful': 0,
            'success_rate': 0
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    email = os.getenv('NAUKRI_EMAIL')
    password = os.getenv('NAUKRI_PASSWORD')
    
    has_credentials = bool(email and password and email != 'set in .env file')
    
    return jsonify({
        'status': 'healthy',
        'credentials_configured': has_credentials,
        'data_directory_exists': os.path.exists('data'),
        'logs_exist': os.path.exists('data/logs/app.log')
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    logger.info(f"Starting Naukri Automation Web UI on http://localhost:{port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
