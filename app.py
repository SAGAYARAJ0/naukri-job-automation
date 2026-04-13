"""
Minimal Web interface for Naukri Job Automation - Vercel Production
Optimized for serverless with zero heavy imports at startup
"""

from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime

# Minimal setup - NO heavy imports here
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# Track if we've attempted orchestrator load
_orchestrator = None
_load_attempted = False


def safe_get_orchestrator():
    """Safely load orchestrator on demand, never fail"""
    global _orchestrator, _load_attempted
    
    if _load_attempted:
        return _orchestrator
    
    _load_attempted = True
    
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from main import Orchestrator
        _orchestrator = Orchestrator()
        logger.info("✓ Orchestrator loaded successfully")
        return _orchestrator
        
    except Exception as e:
        logger.warning(f"⚠ Could not load Orchestrator: {str(e)[:100]}")
        return None


@app.route('/')
def index():
    """Serve the web UI"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return f"<html><body><h1>Naukri Job Automation</h1><p>Error loading UI: {str(e)[:50]}</p></body></html>", 500


@app.route('/api/health', methods=['GET'])
def health():
    """Always respond with health status"""
    try:
        orch = safe_get_orchestrator()
        return jsonify({
            "status": "operational" if orch else "initializing",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "platform": "vercel",
            "orchestrator": "ready" if orch else "loading"
        }), 200
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({"status": "error", "error": str(e)}), 200  # Return 200 anyway


@app.route('/api/search', methods=['POST'])
def search_jobs():
    """Search and filter jobs"""
    try:
        data = request.get_json() or {}
        
        keywords = data.get('keywords', 'Python')
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        
        location = data.get('location', 'Bangalore')
        experience = int(data.get('experience', 3))
        
        logger.info(f"Search: {keywords} in {location} ({experience}y)")
        
        orch = safe_get_orchestrator()
        
        if not orch:
            # Service not ready - return demo data
            return jsonify({
                "status": "initializing",
                "message": "System initializing, please wait 10-15 seconds",
                "keywords": keywords,
                "location": location,
                "jobs": [],
                "total": 0,
                "applied": 0,
                "demo_mode": True
            }), 202
        
        # Execute search with safety net
        try:
            results = orch.search_and_apply(
                keywords=keywords,
                location=location,
                experience_years=experience,
                max_applications=3
            )
            
            return jsonify({
                "status": "success",
                "keywords": keywords,
                "location": location,
                "jobs": results.get('jobs', []),
                "total": results.get('total', 0),
                "applied": results.get('applied', 0)
            }), 200
            
        except Exception as search_error:
            logger.error(f"Search execution error: {search_error}")
            raise
        
    except Exception as e:
        logger.error(f"Search endpoint error: {str(e)[:100]}")
        return jsonify({
            "status": "error",
            "error": str(e)[:100],
            "jobs": [],
            "total": 0
        }), 500


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get stored applications"""
    try:
        orch = safe_get_orchestrator()
        
        if not orch:
            return jsonify({
                "status": "initializing",
                "jobs": [],
                "total": 0
            }), 202
        
        jobs = orch.get_applications() or []
        
        return jsonify({
            "status": "success",
            "jobs": jobs,
            "total": len(jobs)
        }), 200
        
    except Exception as e:
        logger.error(f"Get jobs error: {str(e)[:100]}")
        return jsonify({
            "status": "error",
            "error": str(e)[:100],
            "jobs": [],
            "total": 0
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    try:
        orch = safe_get_orchestrator()
        
        if not orch:
            return jsonify({
                "status": "initializing",
                "total_applications": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0
            }), 202
        
        stats = orch.get_statistics() or {
            "total_applications": 0,
            "successful": 0,
            "failed": 0,
            "success_rate": 0
        }
        
        return jsonify({
            "status": "success",
            **stats
        }), 200
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)[:100]}")
        return jsonify({
            "status": "error",
            "error": str(e)[:100],
            "total_applications": 0
        }), 500


@app.route('/api/version', methods=['GET'])
def version():
    """Get version info"""
    return jsonify({
        "version": "1.0.0",
        "name": "Naukri Job Automation",
        "platform": "Vercel Serverless",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "status": 404}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 error: {e}")
    return jsonify({"error": "Server error", "status": 500}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    logger.info(f"Starting Naukri Automation on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
