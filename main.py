"""
Main orchestrator for Naukri job automation.
Coordinates all modules for job search, filtering, and application.
"""

import time
import sys
import os
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core import get_logger, get_config, get_driver_manager
from modules.login import get_login_module
from modules.search import get_search_module
from modules.filter import get_filter_module
from modules.apply import get_apply_module
from modules.storage import get_storage_module
from modules.scheduler import get_scheduler_module
from utils.human_behavior import get_human_behavior
from utils.helpers import get_helpers

logger = get_logger(__name__)
config = get_config()
behavior = get_human_behavior()
helpers = get_helpers()


class Orchestrator:
    """Main orchestrator for job automation."""
    
    def __init__(self):
        """Initialize orchestrator."""
        logger.info("=" * 80)
        logger.info("NAUKRI JOB AUTOMATION SYSTEM STARTED")
        logger.info("=" * 80)
        
        self.driver_manager = get_driver_manager()
        self.storage = get_storage_module()
        self.scheduler = get_scheduler_module()
        
        self.stats = {
            'start_time': None,
            'jobs_found': 0,
            'jobs_filtered': 0,
            'jobs_applied': 0,
            'successful_applications': 0,
            'failed_applications': 0
        }
    
    def run_automation(self, email, password, keywords, location, experience):
        """
        Run the complete automation workflow.
        
        Args:
            email: Naukri email
            password: Naukri password
            keywords: List of job keywords
            location: Job location
            experience: Years of experience
        """
        logger.info("Starting automation workflow")
        self.stats['start_time'] = time.time()
        
        try:
            # Initialize driver
            driver = self.driver_manager.get_driver()
            
            # Step 1: Login
            if not self._perform_login(driver, email, password):
                logger.error("Login failed, aborting")
                return False
            
            behavior.random_delay(5, 10)
            
            # Step 2: Search for jobs
            jobs = self._search_jobs(driver, keywords, location, experience)
            if not jobs:
                logger.warning("No jobs found")
                return False
            
            behavior.random_delay(5, 10)
            
            # Step 3: Filter jobs
            filter_module = get_filter_module()
            filtered_jobs = self._filter_jobs(filter_module, jobs)
            if not filtered_jobs:
                logger.warning("No jobs passed filter")
                return False
            
            behavior.random_delay(5, 10)
            
            # Step 4: Apply to jobs
            apply_module = get_apply_module(driver, self.storage)
            self._apply_to_jobs(apply_module, filtered_jobs)
            
            # Step 5: Summary and cleanup
            self._log_summary()
            self.driver_manager.quit_driver()
            
            logger.info("Automation workflow completed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Automation failed: {e}")
            self.driver_manager.quit_driver()
            return False
    
    def _perform_login(self, driver, email, password):
        """Perform login."""
        logger.info("Step 1: Authenticating...")
        
        try:
            login_module = get_login_module(driver)
            result = login_module.login(email, password)
            
            if result['status'] == 'success':
                logger.info("[OK] Login successful")
                return True
            elif result['status'] == 'captcha_required':
                logger.warning("CAPTCHA required - manually solve it in the browser")
                time.sleep(30)  # Wait for manual solving
                return True
            else:
                logger.error(f"Login failed: {result['message']}")
                return False
        
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def _search_jobs(self, driver, keywords, location, experience):
        """Search for jobs."""
        logger.info("Step 2: Searching for jobs...")
        
        try:
            search_module = get_search_module(driver)
            jobs = search_module.search_jobs(keywords, location, experience)
            
            self.stats['jobs_found'] = len(jobs)
            logger.info(f"[OK] Found {len(jobs)} jobs")
            
            return jobs
        
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def _filter_jobs(self, filter_module, jobs):
        """Filter jobs."""
        logger.info("Step 3: Filtering jobs...")
        
        try:
            filtered = filter_module.batch_filter(jobs)
            
            self.stats['jobs_filtered'] = len(filtered)
            logger.info(f"[OK] Filtered to {len(filtered)} jobs")
            
            return filtered
        
        except Exception as e:
            logger.error(f"Filter error: {e}")
            return []
    
    def _apply_to_jobs(self, apply_module, jobs):
        """Apply to jobs."""
        logger.info("Step 4: Applying to jobs...")
        
        for idx, job in enumerate(jobs, 1):
            try:
                logger.info(f"Job {idx}/{len(jobs)}: {job.get('title')}")
                
                result = apply_module.apply_to_job(job)
                
                if result['status'] == 'success':
                    self.stats['successful_applications'] += 1
                    logger.info(f"[OK] Application successful")
                elif result['status'] == 'already_applied':
                    logger.info(f"⊗ Already applied")
                elif result['status'] == 'external':
                    logger.info(f"⊗ External redirect")
                else:
                    self.stats['failed_applications'] += 1
                    logger.warning(f"[FAILED] Application failed: {result['message']}")
                
                self.stats['jobs_applied'] += 1
                
                # Pace between applications
                if idx < len(jobs):
                    behavior.random_delay(10, 20)
            
            except Exception as e:
                logger.error(f"Error applying to job: {e}")
                continue
    
    def _log_summary(self):
        """Log execution summary."""
        duration = time.time() - self.stats['start_time']
        
        logger.info("=" * 80)
        logger.info("EXECUTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Duration: {helpers.format_duration(duration)}")
        logger.info(f"Jobs found: {self.stats['jobs_found']}")
        logger.info(f"Jobs filtered: {self.stats['jobs_filtered']}")
        logger.info(f"Jobs applied: {self.stats['jobs_applied']}")
        logger.info(f"Successful applications: {self.stats['successful_applications']}")
        logger.info(f"Failed applications: {self.stats['failed_applications']}")
        logger.info(f"Total applications in storage: {self.storage.get_application_count()}")
        logger.info("=" * 80)
    
    def schedule_automation(self, email, password, keywords, location, experience, 
                          schedule_type='daily', hours=24, start_hour=9):
        """Schedule automation to run periodically."""
        logger.info("Setting up scheduled automation")
        
        def callback():
            return self.run_automation(email, password, keywords, location, experience)
        
        if schedule_type == 'daily':
            job_id = self.scheduler.add_daily_job(callback, hour=start_hour)
        elif schedule_type == 'interval':
            job_id = self.scheduler.add_interval_job(callback, minutes=int(hours * 60))
        elif schedule_type == 'cron':
            # Custom cron expression
            job_id = self.scheduler.add_cron_job(callback, hours)
        else:
            logger.error(f"Unknown schedule type: {schedule_type}")
            return False
        
        if job_id:
            self.scheduler.start()
            logger.info(f"Scheduled job created: {job_id}")
            return True
        
        return False


def main():
    """Main entry point."""
    logger.info("Naukri Job Automation System initialized")
    
    # Example usage
    orchestrator = Orchestrator()
    
    # Get credentials from environment variables (preferred) or config file (fallback)
    try:
        # Priority 1: Environment variables
        email = os.getenv('NAUKRI_EMAIL')
        password = os.getenv('NAUKRI_PASSWORD')
        
        # Priority 2: Config file
        if not email or not password:
            logger.info("No environment variables found, checking config file...")
            config_data = config.get_all()
            email = config_data.get('credentials', {}).get('email')
            password = config_data.get('credentials', {}).get('password')
        
        # Validate credentials
        if not email or not password or email == 'set in .env file':
            logger.error("Credentials not found!")
            logger.info("Please create a .env file with:")
            logger.info("  NAUKRI_EMAIL=your-email@example.com")
            logger.info("  NAUKRI_PASSWORD=your-password")
            logger.info("")
            logger.info("Or add to config/config.json credentials section")
            return
        
        logger.info(f"Using credentials: {email[:10]}***@****")
        
        # Run automation
        keywords = ['Python', 'Backend', 'Django']
        location = 'Bangalore'
        experience = 3
        
        success = orchestrator.run_automation(email, password, keywords, location, experience)
        
        if success:
            logger.info("[OK] Automation completed successfully")
        else:
            logger.error("[FAILED] Automation failed")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
