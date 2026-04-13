"""
Scheduler module for Naukri automation.
Handles periodic job search and application scheduling.
"""

import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from core.logger import get_logger
from core.config_manager import get_config
from utils.helpers import get_helpers

logger = get_logger(__name__)
config = get_config()
helpers = get_helpers()


class SchedulerModule:
    """Manages job scheduling for automation."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.scheduler = BackgroundScheduler()
        self.execution_history = []
        logger.info("Scheduler initialized")
    
    def add_interval_job(self, callback, minutes=30, job_id=None):
        """Add interval-based scheduled job."""
        try:
            job_id = job_id or f"interval_{int(time.time())}"
            
            self.scheduler.add_job(
                func=self._wrap_callback(callback),
                trigger=IntervalTrigger(minutes=minutes),
                id=job_id,
                name=f"Every {minutes} minutes",
                misfire_grace_time=60
            )
            
            logger.info(f"Interval job added: {job_id} (every {minutes} min)")
            return job_id
        
        except Exception as e:
            logger.error(f"Failed to add interval job: {e}")
            return None
    
    def add_cron_job(self, callback, cron_expression, job_id=None):
        """Add cron-based scheduled job."""
        try:
            job_id = job_id or f"cron_{int(time.time())}"
            
            self.scheduler.add_job(
                func=self._wrap_callback(callback),
                trigger=CronTrigger.from_crontab(cron_expression),
                id=job_id,
                name=f"Cron: {cron_expression}",
                misfire_grace_time=60
            )
            
            logger.info(f"Cron job added: {job_id} ({cron_expression})")
            return job_id
        
        except Exception as e:
            logger.error(f"Failed to add cron job: {e}")
            return None
    
    def add_daily_job(self, callback, hour=9, minute=0, job_id=None):
        """Add daily job at specific time."""
        try:
            job_id = job_id or f"daily_{int(time.time())}"
            cron = f"{minute} {hour} * * *"
            
            return self.add_cron_job(callback, cron, job_id)
        
        except Exception as e:
            logger.error(f"Failed to add daily job: {e}")
            return None
    
    def _wrap_callback(self, callback):
        """Wrap callback to track execution."""
        def wrapped():
            try:
                logger.info("Executing scheduled job")
                start_time = time.time()
                
                result = callback()
                
                duration = time.time() - start_time
                execution_record = {
                    'timestamp': helpers.get_timestamp(),
                    'duration': duration,
                    'status': 'success',
                    'result': str(result)
                }
                
                logger.info(f"Job executed successfully ({duration:.2f}s)")
            
            except Exception as e:
                logger.error(f"Scheduled job failed: {e}")
                execution_record = {
                    'timestamp': helpers.get_timestamp(),
                    'duration': 0,
                    'status': 'failed',
                    'error': str(e)
                }
            
            self.execution_history.append(execution_record)
        
        return wrapped
    
    def start(self):
        """Start scheduler."""
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                logger.info("Scheduler started")
                return True
            else:
                logger.warning("Scheduler already running")
                return False
        
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            return False
    
    def stop(self):
        """Stop scheduler gracefully."""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("Scheduler stopped")
                return True
            else:
                logger.warning("Scheduler not running")
                return False
        
        except Exception as e:
            logger.error(f"Failed to stop scheduler: {e}")
            return False
    
    def pause_job(self, job_id):
        """Pause a scheduled job."""
        try:
            self.scheduler.pause_job(job_id)
            logger.info(f"Job paused: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to pause job: {e}")
            return False
    
    def resume_job(self, job_id):
        """Resume a paused job."""
        try:
            self.scheduler.resume_job(job_id)
            logger.info(f"Job resumed: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to resume job: {e}")
            return False
    
    def remove_job(self, job_id):
        """Remove a scheduled job."""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Job removed: {job_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove job: {e}")
            return False
    
    def get_jobs(self):
        """Get list of scheduled jobs."""
        return self.scheduler.get_jobs()
    
    def get_execution_history(self):
        """Get execution history."""
        return self.execution_history


# Singleton instance
scheduler_module = None

def get_scheduler_module():
    """Get scheduler module instance."""
    global scheduler_module
    if scheduler_module is None:
        scheduler_module = SchedulerModule()
    return scheduler_module
