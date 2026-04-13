"""
Storage module for Naukri automation.
Persists applied jobs and prevents duplicates using JSON/SQLite.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from core.logger import get_logger
from core.config_manager import get_config
from core.exceptions import StorageException
from utils.helpers import get_helpers

logger = get_logger(__name__)
config = get_config()
helpers = get_helpers()


class StorageModule:
    """Handles persistence of applied jobs."""
    
    def __init__(self, storage_type=None):
        """Initialize storage module."""
        self.storage_type = storage_type or config.get('storage.type', 'json')
        self.json_file = Path(__file__).parent.parent / "data" / "applied_jobs.json"
        self.db_file = Path(__file__).parent.parent / "data" / "jobs.db"
        
        # Create data directory
        self.json_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize storage
        if self.storage_type == 'json':
            self._init_json()
        elif self.storage_type == 'sqlite':
            self._init_sqlite()
        
        logger.info(f"Storage module initialized ({self.storage_type})")
    
    def _init_json(self):
        """Initialize JSON storage."""
        if not self.json_file.exists():
            initial_data = {
                'applications': [],
                'metadata': {
                    'total_applications': 0,
                    'successful': 0,
                    'failed': 0,
                    'external': 0,
                    'already_applied': 0,
                    'last_updated': helpers.get_timestamp()
                }
            }
            helpers.save_json(initial_data, str(self.json_file))
            logger.info(f"JSON storage initialized at {self.json_file}")
    
    def _init_sqlite(self):
        """Initialize SQLite storage."""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT UNIQUE,
                    title TEXT,
                    url TEXT,
                    status TEXT,
                    applied_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info(f"SQLite storage initialized at {self.db_file}")
        
        except Exception as e:
            logger.error(f"Failed to initialize SQLite: {e}")
            raise StorageException(f"SQLite initialization failed: {e}")
    
    def save_applied_job(self, job_id, title, url, status):
        """Save applied job record."""
        logger.info(f"Saving applied job: {job_id}")
        
        try:
            if self.storage_type == 'json':
                self._save_json(job_id, title, url, status)
            elif self.storage_type == 'sqlite':
                self._save_sqlite(job_id, title, url, status)
            
            logger.debug(f"Job saved: {job_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to save job: {e}")
            return False
    
    def _save_json(self, job_id, title, url, status):
        """Save to JSON storage."""
        data = helpers.load_json(str(self.json_file)) or {'applications': [], 'metadata': {}}
        
        # Check if already exists
        for app in data.get('applications', []):
            if app.get('job_id') == job_id:
                logger.debug(f"Job {job_id} already in storage")
                return
        
        # Add new application
        record = {
            'job_id': job_id,
            'title': title,
            'url': url,
            'status': status,
            'applied_at': helpers.get_timestamp()
        }
        
        data['applications'].append(record)
        
        # Update metadata
        data['metadata']['total_applications'] = len(data['applications'])
        data['metadata']['last_updated'] = helpers.get_timestamp()
        
        if status == 'success':
            data['metadata']['successful'] = data['metadata'].get('successful', 0) + 1
        
        helpers.save_json(data, str(self.json_file))
    
    def _save_sqlite(self, job_id, title, url, status):
        """Save to SQLite storage."""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO applications (job_id, title, url, status, applied_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (job_id, title, url, status, helpers.get_timestamp()))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            logger.error(f"SQLite save error: {e}")
            raise
    
    def is_already_applied(self, job_id):
        """Check if job was already applied to."""
        try:
            if self.storage_type == 'json':
                return self._is_applied_json(job_id)
            elif self.storage_type == 'sqlite':
                return self._is_applied_sqlite(job_id)
            
            return False
        
        except Exception as e:
            logger.error(f"Check error: {e}")
            return False  # Assume not applied if error
    
    def _is_applied_json(self, job_id):
        """Check JSON storage."""
        data = helpers.load_json(str(self.json_file))
        if not data:
            return False
        
        for app in data.get('applications', []):
            if app.get('job_id') == job_id:
                logger.debug(f"Job {job_id} already applied")
                return True
        
        return False
    
    def _is_applied_sqlite(self, job_id):
        """Check SQLite storage."""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM applications WHERE job_id = ?', (job_id,))
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
        
        except Exception as e:
            logger.error(f"SQLite check error: {e}")
            return False
    
    def get_application_count(self):
        """Get total application count."""
        try:
            if self.storage_type == 'json':
                data = helpers.load_json(str(self.json_file)) or {}
                return len(data.get('applications', []))
            
            elif self.storage_type == 'sqlite':
                conn = sqlite3.connect(str(self.db_file))
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM applications')
                count = cursor.fetchone()[0]
                conn.close()
                return count
        
        except Exception as e:
            logger.error(f"Count error: {e}")
            return 0
    
    def get_statistics(self):
        """Get storage statistics."""
        try:
            if self.storage_type == 'json':
                data = helpers.load_json(str(self.json_file)) or {}
                return data.get('metadata', {})
            
            elif self.storage_type == 'sqlite':
                conn = sqlite3.connect(str(self.db_file))
                cursor = conn.cursor()
                
                cursor.execute('SELECT COUNT(*) FROM applications')
                total = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'success'")
                success = cursor.fetchone()[0]
                
                conn.close()
                
                return {
                    'total_applications': total,
                    'successful': success,
                    'failure_rate': (total - success) / total if total > 0 else 0
                }
        
        except Exception as e:
            logger.error(f"Statistics error: {e}")
            return {}
    
    def export_history(self, filepath=None, format='json'):
        """Export application history."""
        try:
            filepath = filepath or f"data/export_{helpers.get_date_str()}.{format}"
            
            if self.storage_type == 'json':
                data = helpers.load_json(str(self.json_file))
            else:
                data = self._get_all_from_sqlite()
            
            if format == 'json':
                helpers.save_json(data, filepath)
            
            logger.info(f"History exported to {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Export error: {e}")
            return None
    
    def _get_all_from_sqlite(self):
        """Get all records from SQLite."""
        try:
            conn = sqlite3.connect(str(self.db_file))
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM applications')
            columns = [description[0] for description in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return records
        
        except Exception as e:
            logger.error(f"SQLite retrieval error: {e}")
            return []


# Singleton instance
storage_module = None

def get_storage_module(storage_type=None):
    """Get storage module instance."""
    global storage_module
    if storage_module is None:
        storage_module = StorageModule(storage_type)
    return storage_module
