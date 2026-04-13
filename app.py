"""
Web interface for Naukri Job Automation System - Vercel-optimized version
Lightweight Flask app for serverless deployment
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.warning("python-dotenv not installed, using environment variables only")
    pass

# Global state
orchestrator = None
initialized = False

def get_orchestrator():
    """Lazy initialization of Orchestrator"""
    global orchestrator, initialized
    
    if initialized:
        return orchestrator
    
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from main import Orchestrator
        
        orchestrator = Orchestrator()
        initialized = True
        logger.info("Orchestrator initialized successfully")
        return orchestrator
        
    except Exception as e:
        logger.error(f"Failed to initialize Orchestrator: {str(e)}")
        initialized = True  # Mark as initialized to avoid repeated attempts
        return None


@app.route('/')
def index():
    """Home page with search form"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error loading index: {str(e)}")
        return jsonify({"error": "Failed to load UI"}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        orch = get_orchestrator()
        status = "operational" if orch else "degraded"
        return jsonify({
            "status": status,
            "message": "Naukri Automation Service" if orch else "Service starting up",
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search_jobs():
    """API endpoint for job search"""
    try:
        data = request.json or {}
        
        keywords = data.get('keywords', 'Python')
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        
        location = data.get('location', 'Bangalore')
        experience = int(data.get('experience', 3))
        freshness = data.get('freshness', '7')
        
        logger.info(f"Search request: {keywords}, {location}, {experience}yrs, within {freshness} days")
        
        # Try to get orchestrator
        orch = get_orchestrator()
        
        if not orch:
            return jsonify({
                "status": "pending",
                "message": "Service initializing. Please try again in a moment.",
                "jobs": [],
                "total": 0
            }), 202  # Accepted but processing
        
        # Execute search
        results = orch.search_and_apply(
            keywords=keywords,
            location=location,
            experience_years=experience,
            max_applications=5  # Limit for serverless
        )
        
        return jsonify({
            "status": "success",
            "keywords": keywords,
            "location": location,
            "experience": experience,
            "jobs": results.get('jobs', []),
            "total": results.get('total', 0),
            "applied": results.get('applied', 0)
        }), 200
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Search failed. Check logs for details."
        }), 500


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get application history"""
    try:
        orch = get_orchestrator()
        
        if not orch:
            return jsonify({
                "status": "pending",
                "message": "Service initializing",
                "jobs": []
            }), 202
        
        jobs = orch.get_applications()
        
        return jsonify({
            "status": "success",
            "jobs": jobs if jobs else [],
            "total": len(jobs) if jobs else 0
        }), 200
        
    except Exception as e:
        logger.error(f"Get jobs error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "jobs": []
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    try:
        orch = get_orchestrator()
        
        if not orch:
            return jsonify({
                "status": "pending",
                "total_applications": 0,
                "successful": 0,
                "failed": 0,
                "pending": 0
            }), 202
        
        stats = orch.get_statistics()
        
        return jsonify({
            "status": "success",
            **stats
        }), 200
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found", "status": 404}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error", "status": 500}), 500


if __name__ == '__main__':
    # Local development
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    logger.info(f"Starting on port {port} (debug={debug})")
    app.run(debug=debug, host='0.0.0.0', port=port)
        
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
