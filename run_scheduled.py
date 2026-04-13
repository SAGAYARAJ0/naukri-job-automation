"""
Scheduled runner for Naukri automation.
Run this script to start scheduled automation.
"""

import sys
import logging
from pathlib import Path
from main import Orchestrator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_scheduled_automation():
    """Run scheduled automation."""
    
    logger.info("Initializing scheduled automation...")
    
    orchestrator = Orchestrator()
    
    # Configuration from config file
    from core import get_config
    config = get_config()
    
    try:
        # Get credentials
        email = config.get('credentials.email')
        password = config.get('credentials.password')
        
        if email == "your-email@example.com" or password == "your-password":
            logger.error("❌ Please update credentials in config/config.json")
            return False
        
        # Get search criteria
        filters = config.load_filters()
        
        keywords = filters.get('required_skills', ['Python'])
        location = filters.get('preferred_locations', ['Bangalore'])[0]
        experience = filters.get('min_experience', 0)
        
        logger.info(f"Starting job automation...")
        logger.info(f"  Keywords: {keywords}")
        logger.info(f"  Location: {location}")
        logger.info(f"  Experience: {experience}+ years")
        
        # Run automation
        success = orchestrator.run_automation(
            email, 
            password, 
            keywords, 
            location, 
            experience
        )
        
        if success:
            logger.info("✓ Automation completed")
        else:
            logger.error("✗ Automation failed")
        
        return success
    
    except Exception as e:
        logger.error(f"ERROR: {e}")
        return False


def setup_daily_schedule():
    """Setup daily scheduled automation."""
    
    logger.info("Setting up daily automation schedule...")
    
    orchestrator = Orchestrator()
    
    from core import get_config
    config = get_config()
    
    try:
        email = config.get('credentials.email')
        password = config.get('credentials.password')
        filters = config.load_filters()
        
        if email == "your-email@example.com":
            logger.error("❌ Please update credentials first")
            return False
        
        keywords = filters.get('required_skills', ['Python'])
        location = filters.get('preferred_locations', ['Bangalore'])[0]
        experience = filters.get('min_experience', 0)
        
        # Schedule daily at 9 AM
        success = orchestrator.schedule_automation(
            email,
            password,
            keywords,
            location,
            experience,
            schedule_type='daily',
            start_hour=9
        )
        
        if success:
            logger.info("✓ Daily schedule setup complete")
            logger.info("  The system will run every day at 9:00 AM")
            logger.info("  Keep this script running to maintain the schedule")
            
            # Keep scheduler running
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Schedule stopped by user")
                return True
        else:
            logger.error("✗ Failed to setup schedule")
            return False
    
    except Exception as e:
        logger.error(f"ERROR: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        setup_daily_schedule()
    else:
        run_scheduled_automation()
