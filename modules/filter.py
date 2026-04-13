"""
Job filter module for Naukri automation.
Filters jobs based on skills, experience, and relevance.
"""

import re
from core.logger import get_logger
from core.config_manager import get_config
from core.exceptions import FilterException
from utils.helpers import get_helpers

logger = get_logger(__name__)
config = get_config()
helpers = get_helpers()


class FilterModule:
    """Filters jobs based on user criteria."""
    
    def __init__(self):
        """Initialize filter module."""
        self.filter_config = config.load_filters()
    
    def filter_job(self, job_data, user_profile=None):
        """
        Filter a job based on criteria.
        
        Args:
            job_data: Job dictionary from search
            user_profile: User profile with skills and experience
        
        Returns:
            {decision: bool, score: float, details: dict}
        """
        logger.debug(f"Filtering job: {job_data.get('title')}")
        
        try:
            if user_profile is None:
                user_profile = self._get_default_profile()
            
            # Calculate component scores
            skill_score = self._calculate_skill_match(job_data, user_profile)
            exp_score = self._calculate_experience_match(job_data, user_profile)
            red_flag_score = self._check_red_flags(job_data)
            
            # Final weighted score
            final_score = (skill_score * 0.5) + (exp_score * 0.3) + (red_flag_score * 0.2)
            
            # Decision
            threshold = self.filter_config.get('filter_threshold', 70)
            decision = final_score >= threshold
            
            details = {
                'skill_score': skill_score,
                'experience_score': exp_score,
                'red_flag_score': red_flag_score,
                'final_score': final_score,
                'threshold': threshold
            }
            
            logger.debug(f"Filter result: {decision} (score: {final_score})")
            
            return {
                'decision': decision,
                'score': final_score,
                'details': details
            }
        
        except Exception as e:
            logger.error(f"Filter error: {e}")
            raise FilterException(f"Job filtering failed: {e}")
    
    def _calculate_skill_match(self, job_data, user_profile):
        """Calculate skill matching score (0-100)."""
        logger.debug("Calculating skill match")
        
        try:
            user_skills = set(s.lower() for s in user_profile.get('skills', []))
            if not user_skills:
                return 50  # Default if no user skills
            
            # Extract skills from job title and company
            job_text = f"{job_data.get('title', '')} {job_data.get('company', '')}".lower()
            
            matched_skills = 0
            for skill in user_skills:
                if skill in job_text:
                    matched_skills += 1
            
            score = (matched_skills / len(user_skills)) * 100
            logger.debug(f"Skill match: {matched_skills}/{len(user_skills)} = {score}%")
            
            return score
        
        except Exception as e:
            logger.warning(f"Skill calculation error: {e}")
            return 50
    
    def _calculate_experience_match(self, job_data, user_profile):
        """Calculate experience requirement match (0-100)."""
        logger.debug("Calculating experience match")
        
        try:
            user_exp = user_profile.get('experience', 0)
            
            # Extract experience requirement from job
            job_text = f"{job_data.get('title', '')} {job_data.get('company', '')}".lower()
            
            # Try to extract years from text (e.g., "3 years", "3+")
            exp_match = re.search(r'(\d+)\+?\s*years?', job_text)
            required_exp = int(exp_match.group(1)) if exp_match else 0
            
            if required_exp == 0:
                return 100  # No requirement found, neutral
            
            # Calculate match
            if user_exp >= required_exp:
                score = 100
            else:
                gap = required_exp - user_exp
                max_gap = config.get('filter.min_experience_gap', 2)
                
                if gap > max_gap:
                    score = 0  # Too much gap
                else:
                    score = (1 - (gap / max_gap)) * 100
            
            logger.debug(f"Experience match: user={user_exp}yr, required={required_exp}yr, score={score}%")
            
            return score
        
        except Exception as e:
            logger.warning(f"Experience calculation error: {e}")
            return 50
    
    def _check_red_flags(self, job_data):
        """Check for red flags (0-100, 100 is good)."""
        logger.debug("Checking red flags")
        
        try:
            red_flags_list = self.filter_config.get('red_flags', [])
            job_text = f"{job_data.get('title', '')} {job_data.get('company', '')}".lower()
            
            found_flags = 0
            for flag in red_flags_list:
                if flag.lower() in job_text:
                    found_flags += 1
                    logger.warning(f"Red flag detected: {flag}")
            
            # Score inversely (flags reduce score)
            if found_flags > 0:
                score = max(0, 100 - (found_flags * 20))
            else:
                score = 100
            
            logger.debug(f"Red flags: {found_flags} found, score={score}%")
            
            return score
        
        except Exception as e:
            logger.warning(f"Red flag check error: {e}")
            return 100
    
    def _get_default_profile(self):
        """Get default user profile."""
        return {
            'skills': self.filter_config.get('required_skills', []),
            'experience': self.filter_config.get('min_experience', 0),
            'locations': self.filter_config.get('preferred_locations', [])
        }
    
    def batch_filter(self, jobs, user_profile=None):
        """Filter multiple jobs."""
        logger.info(f"Batch filtering {len(jobs)} jobs")
        
        filtered_jobs = []
        for job in jobs:
            try:
                result = self.filter_job(job, user_profile)
                if result['decision']:
                    filtered_jobs.append({**job, 'filter_score': result['score']})
            except Exception as e:
                logger.debug(f"Failed to filter job: {e}")
                continue
        
        logger.info(f"Batch filter result: {len(filtered_jobs)} jobs passed")
        return filtered_jobs


# Singleton instance
filter_module = None

def get_filter_module():
    """Get filter module instance."""
    global filter_module
    if filter_module is None:
        filter_module = FilterModule()
    return filter_module
