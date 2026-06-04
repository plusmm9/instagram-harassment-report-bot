#!/usr/bin/env python3
"""
Instagram Harassment Report Bot - Core Module
Mass reporting tool for Instagram accounts engaged in harassment

Legal Notice: Use this tool responsibly and only for legitimate reporting.
Report only accounts that genuinely violate Instagram's Community Guidelines.
"""

import requests
import time
import json
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import random
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('harassment_reports.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InstagramHarassmentReporter:
    """Mass harassment report bot for Instagram accounts"""
    
    # Instagram API endpoints
    BASE_URL = "https://www.instagram.com/api/v1"
    WEB_URL = "https://www.instagram.com"
    
    # Report reason IDs
    REPORT_REASONS = {
        'harassment': '8',
        'spam': '3',
        'fake_account': '7',
        'scam': '13',
        'impersonation': '6',
        'hate_speech': '12',
    }
    
    def __init__(self, session_id: str = None, user_agent: str = None):
        """
        Initialize the reporter
        
        Args:
            session_id: Instagram session ID (from authenticated browser session)
            user_agent: Custom user agent string
        """
        self.session_id = session_id
        self.user_agent = user_agent or self._get_default_user_agent()
        self.session = requests.Session()
        self.session.headers.update(self._get_default_headers())
        self.reports_sent = 0
        self.reports_failed = 0
        self.user_cache = {}  # Cache user IDs to avoid repeated lookups
        
    def _get_default_user_agent(self) -> str:
        """Get a random Instagram mobile user agent"""
        agents = [
            'Instagram 200.0.0.0.0 Android (28/9.0; 1080x1920; 3; samsung; SM-G950F)',
            'Instagram 210.0.0.0.0 Android (29/10; 1440x2960; 2.5; google; Pixel 3 XL)',
            'Instagram 220.0.0.0.0 Android (30/11; 1080x2340; 2.5; oneplus; GM1915)',
            'Instagram 230.0.0.0.0 Android (31/12; 1440x3120; 2.5; oneplus; IN2020)',
            'Instagram 240.0.0.0.0 Android (32/12L; 1080x2400; 2.75; samsung; SM-A515F)',
        ]
        return random.choice(agents)
    
    def _get_default_headers(self) -> Dict:
        """Get default request headers"""
        return {
            'User-Agent': self.user_agent,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
        }
    
    def get_user_id(self, username: str) -> Optional[str]:
        """
        Get Instagram user ID from username
        
        Args:
            username: Instagram username
            
        Returns:
            User ID or None if not found
        """
        # Check cache first
        if username in self.user_cache:
            logger.debug(f"Using cached user ID for {username}")
            return self.user_cache[username]
        
        try:
            url = f"{self.BASE_URL}/users/web_profile_info/"
            params = {'username': username}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            user_id = data.get('data', {}).get('user', {}).get('id')
            
            if user_id:
                user_id_str = str(user_id)
                self.user_cache[username] = user_id_str  # Cache it
                logger.info(f"✓ Found user ID for @{username}: {user_id_str}")
                return user_id_str
            else:
                logger.warning(f"✗ Could not find user ID for @{username}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"✗ Timeout fetching user ID for @{username}")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"✗ User not found: @{username}")
            else:
                logger.error(f"✗ HTTP error fetching user ID for @{username}: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"✗ Error fetching user ID for @{username}: {str(e)}")
            return None
    
    def report_harassment(self, username: str, user_id: str = None, reason: str = 'harassment') -> bool:
        """
        Report an account for harassment
        
        Args:
            username: Instagram username to report
            user_id: User ID (will be fetched if not provided)
            reason: Report reason (default: 'harassment')
            
        Returns:
            True if report was sent successfully, False otherwise
        """
        try:
            # Get user ID if not provided
            if not user_id:
                user_id = self.get_user_id(username)
                if not user_id:
                    logger.error(f"✗ Could not fetch user ID for @{username}")
                    self.reports_failed += 1
                    return False
            
            # Instagram report endpoint
            url = f"{self.BASE_URL}/users/{user_id}/report/"
            
            # Get reason ID
            reason_id = self.REPORT_REASONS.get(reason, self.REPORT_REASONS['harassment'])
            
            # Report payload
            payload = {
                'user_id': user_id,
                'source_name': 'profile',
                'reason_id': reason_id,
                'frx_context': ''
            }
            
            headers = self.session.headers.copy()
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
            response = self.session.post(url, data=payload, headers=headers, timeout=15)
            
            if response.status_code in [200, 201, 204]:
                logger.info(f"✓ Successfully reported @{username} ({user_id}) for {reason}")
                self.reports_sent += 1
                return True
            elif response.status_code == 429:
                logger.warning(f"⚠ Rate limited for @{username}. Try again later.")
                self.reports_failed += 1
                return False
            else:
                logger.warning(f"✗ Failed to report @{username}: HTTP {response.status_code}")
                self.reports_failed += 1
                return False
                
        except requests.exceptions.Timeout:
            logger.error(f"✗ Timeout reporting @{username}")
            self.reports_failed += 1
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Network error reporting @{username}: {str(e)}")
            self.reports_failed += 1
            return False
        except Exception as e:
            logger.error(f"✗ Unexpected error reporting @{username}: {str(e)}")
            self.reports_failed += 1
            return False
    
    def report_multiple(self, usernames: List[str], delay: float = 2.0, reason: str = 'harassment') -> Dict:
        """
        Report multiple accounts for harassment
        
        Args:
            usernames: List of Instagram usernames to report
            delay: Delay between reports in seconds (default 2.0)
            reason: Report reason (default: 'harassment')
            
        Returns:
            Dictionary with report statistics
        """
        if not usernames:
            logger.error("No usernames provided")
            return {'total': 0, 'successful': 0, 'failed': 0}
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting mass {reason} report for {len(usernames)} accounts")
        logger.info(f"Delay between reports: {delay}s")
        logger.info(f"{'='*60}\n")
        
        start_time = datetime.now()
        
        for i, username in enumerate(usernames, 1):
            logger.info(f"[{i}/{len(usernames)}] @{username}")
            
            self.report_harassment(username, reason=reason)
            
            # Add random jitter to delay
            jittered_delay = delay + random.uniform(-0.5, 0.5)
            
            if i < len(usernames):
                time.sleep(max(0.5, jittered_delay))  # Ensure minimum delay
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        stats = {
            'total': len(usernames),
            'successful': self.reports_sent,
            'failed': self.reports_failed,
            'success_rate': (self.reports_sent / len(usernames) * 100) if usernames else 0,
            'duration_seconds': duration,
            'timestamp': datetime.now().isoformat()
        }
        
        self._print_summary(stats)
        return stats
    
    def _print_summary(self, stats: Dict):
        """Print a formatted summary of results"""
        print(f"\n{'='*60}")
        print(f"REPORTING SUMMARY")
        print(f"{'='*60}")
        print(f"Total accounts:     {stats['total']}")
        print(f"Successful:         {stats['successful']} ✓")
        print(f"Failed:             {stats['failed']} ✗")
        print(f"Success rate:       {stats['success_rate']:.1f}%")
        print(f"Duration:           {stats['duration_seconds']:.1f}s")
        print(f"{'='*60}\n")
    
    def load_targets_from_file(self, filepath: str) -> List[str]:
        """
        Load target usernames from a file
        
        Args:
            filepath: Path to file containing usernames (one per line)
            
        Returns:
            List of usernames
        """
        try:
            with open(filepath, 'r') as f:
                usernames = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
            logger.info(f"✓ Loaded {len(usernames)} usernames from {filepath}")
            return usernames
        except FileNotFoundError:
            logger.error(f"✗ File not found: {filepath}")
            return []
        except Exception as e:
            logger.error(f"✗ Error reading file {filepath}: {str(e)}")
            return []
    
    def save_report_stats(self, stats: Dict, filepath: str = 'report_stats.json'):
        """
        Save report statistics to a JSON file
        
        Args:
            stats: Statistics dictionary
            filepath: Output file path
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(stats, f, indent=2)
            logger.info(f"✓ Report statistics saved to {filepath}")
        except Exception as e:
            logger.error(f"✗ Error saving statistics: {str(e)}")


def main():
    """
    Main function - example usage
    """
    print("""
    ╔════════════════════════════════════════════════╗
    ║    Instagram Harassment Report Bot v1.0        ║
    ║    Professional Mass Reporting Tool            ║
    ╚════════════════════════════════════════════════╝
    
    ⚠️  LEGAL NOTICE:
    Use this tool responsibly and only for legitimate reporting.
    Report only accounts that genuinely violate Instagram's
    Community Guidelines. Misuse may result in legal consequences.
    """)
    
    # Initialize the reporter
    reporter = InstagramHarassmentReporter()
    
    # Load targets from file
    usernames = reporter.load_targets_from_file('targets.txt')
    
    if not usernames:
        print("\n✗ No targets loaded. Please add usernames to targets.txt")
        print("\nExample targets.txt:")
        print("fake_account_123")
        print("spam_bot_456")
        print("harassing_user_789")
        return
    
    # Report harassment
    stats = reporter.report_multiple(usernames, delay=2.0, reason='harassment')
    
    # Save results
    reporter.save_report_stats(stats)
    print(f"\n✓ Complete! Check harassment_reports.log for details.")


if __name__ == '__main__':
    main()
