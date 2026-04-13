"""
Example usage of Naukri automation system.
This script demonstrates how to use the automation system.
"""

from core import get_logger, get_config
from main import Orchestrator
import time

logger = get_logger(__name__)


def example_single_run():
    """Example: Run automation once."""
    
    print("\n" + "="*80)
    print("EXAMPLE 1: Single Automation Run")
    print("="*80 + "\n")
    
    orchestrator = Orchestrator()
    
    # Configuration
    email = "your-email@naukri.com"
    password = "your-password"
    keywords = ["Python", "Backend Developer"]
    location = "Bangalore"
    experience = 3
    
    # Run
    success = orchestrator.run_automation(
        email=email,
        password=password,
        keywords=keywords,
        location=location,
        experience=experience
    )
    
    if success:
        print("\n✓ Single run completed successfully!")
    else:
        print("\n✗ Single run failed")


def example_scheduled_run():
    """Example: Schedule automation to run daily."""
    
    print("\n" + "="*80)
    print("EXAMPLE 2: Scheduled Automation (Daily)")
    print("="*80 + "\n")
    
    orchestrator = Orchestrator()
    
    # Configuration
    email = "your-email@naukri.com"
    password = "your-password"
    keywords = ["Python", "Backend Developer"]
    location = "Bangalore"
    experience = 3
    
    # Schedule for daily run at 9 AM
    success = orchestrator.schedule_automation(
        email=email,
        password=password,
        keywords=keywords,
        location=location,
        experience=experience,
        schedule_type='daily',
        start_hour=9
    )
    
    if success:
        print("\n✓ Daily schedule setup complete!")
        print("  The system will run every day at 9:00 AM")
        print("  Keep this script running in a terminal/background process")
        print("\n  To stop: Press Ctrl+C\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSchedule stopped")
    else:
        print("\n✗ Schedule setup failed")


def example_interval_schedule():
    """Example: Schedule automation every N hours."""
    
    print("\n" + "="*80)
    print("EXAMPLE 3: Interval Scheduling (Every 12 hours)")
    print("="*80 + "\n")
    
    orchestrator = Orchestrator()
    
    # Configuration
    email = "your-email@naukri.com"
    password = "your-password"
    keywords = ["Python", "Backend Developer"]
    location = "Bangalore"
    experience = 3
    
    # Schedule every 12 hours
    success = orchestrator.schedule_automation(
        email=email,
        password=password,
        keywords=keywords,
        location=location,
        experience=experience,
        schedule_type='interval',
        hours=12
    )
    
    if success:
        print("\n✓ Interval schedule setup complete!")
        print("  The system will run every 12 hours")
        print("  Keep this script running in a terminal/background process\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSchedule stopped")
    else:
        print("\n✗ Schedule setup failed")


def example_with_config():
    """Example: Load configuration from files."""
    
    print("\n" + "="*80)
    print("EXAMPLE 4: Using Configuration Files")
    print("="*80 + "\n")
    
    config = get_config()
    filters = config.load_filters()
    
    # Get configuration
    email = config.get('credentials.email')
    password = config.get('credentials.password')
    
    keywords = filters.get('required_skills', [])
    location = filters.get('preferred_locations', [])[0] if filters.get('preferred_locations') else 'Bangalore'
    experience = filters.get('min_experience', 0)
    
    print(f"Configuration loaded:")
    print(f"  Email: {email}")
    print(f"  Keywords: {keywords}")
    print(f"  Location: {location}")
    print(f"  Min Experience: {experience}+\n")
    
    # Verify credentials are updated
    if email == "your-email@example.com":
        print("⚠️  Please update credentials in config/config.json first!")
        return
    
    orchestrator = Orchestrator()
    success = orchestrator.run_automation(
        email=email,
        password=password,
        keywords=keywords,
        location=location,
        experience=experience
    )
    
    if success:
        print("\n✓ Config-based run completed!")
    else:
        print("\n✗ Run failed")


def example_view_history():
    """Example: View application history."""
    
    print("\n" + "="*80)
    print("EXAMPLE 5: View Application History")
    print("="*80 + "\n")
    
    from modules import get_storage_module
    
    storage = get_storage_module()
    
    # Get statistics
    stats = storage.get_statistics()
    count = storage.get_application_count()
    
    print(f"Total applications: {count}")
    print(f"Statistics: {stats}\n")
    
    # Export history
    export_file = storage.export_history()
    if export_file:
        print(f"✓ History exported to: {export_file}")
    else:
        print("✗ Export failed")


if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("NAUKRI JOB AUTOMATION - USAGE EXAMPLES")
    print("="*80)
    print("\nChoose an example to run:\n")
    print("1. Single automation run")
    print("2. Schedule daily automation")
    print("3. Schedule interval-based automation")
    print("4. Load from configuration files")
    print("5. View application history")
    print("0. Exit\n")
    
    choice = input("Enter your choice (0-5): ").strip()
    
    try:
        if choice == "1":
            example_single_run()
        elif choice == "2":
            example_scheduled_run()
        elif choice == "3":
            example_interval_schedule()
        elif choice == "4":
            example_with_config()
        elif choice == "5":
            example_view_history()
        elif choice == "0":
            print("\nExiting...")
        else:
            print("\n✗ Invalid choice")
    
    except Exception as e:
        logger.error(f"Error running example: {e}")
