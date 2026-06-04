#!/usr/bin/env python3
"""
Advanced Instagram Harassment Report Bot
Features: Batching, retry logic, detailed statistics, and progress tracking
"""

import json
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime
from harassment_report_bot import InstagramHarassmentReporter
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AdvancedHarassmentReporter(InstagramHarassmentReporter):
    """Advanced reporting with batching, retry logic, and statistics"""
    
    def __init__(self, session_id: str = None):
        super().__init__(session_id)
        self.successful_reports = []
        self.failed_reports = []
        self.start_time = None
        self.end_time = None
    
    def report_with_retry(self, username: str, max_retries: int = 3, reason: str = 'harassment') -> bool:
        """
        Report an account with retry logic
        
        Args:
            username: Instagram username
            max_retries: Maximum number of retries
            reason: Report reason
            
        Returns:
            True if successful, False otherwise
        """
        for attempt in range(max_retries):
            try:
                user_id = self.get_user_id(username)
                if not user_id:
                    logger.warning(f"Could not get user ID for @{username} (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(config.RETRY_DELAY)
                    continue
                
                success = self.report_harassment(username, user_id, reason=reason)
                
                if success:
                    self.successful_reports.append({
                        'username': username,
                        'user_id': user_id,
                        'timestamp': datetime.now().isoformat(),
                        'attempt': attempt + 1,
                        'reason': reason
                    })
                    return True
                else:
                    if attempt < max_retries - 1:
                        logger.info(f"Retrying @{username} (attempt {attempt + 2}/{max_retries})...")
                        time.sleep(config.RETRY_DELAY)
                    
            except Exception as e:
                logger.error(f"Error in retry logic for @{username}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(config.RETRY_DELAY)
        
        self.failed_reports.append({
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'reason': 'Max retries exceeded'
        })
        return False
    
    def report_batch(self, usernames: List[str], batch_size: int = None, 
                    delay: float = None, reason: str = 'harassment') -> Dict:
        """
        Report accounts in batches with delays between batches
        
        Args:
            usernames: List of usernames to report
            batch_size: Number of reports per batch
            delay: Delay between individual reports
            reason: Report reason
            
        Returns:
            Statistics dictionary
        """
        batch_size = batch_size or config.BATCH_SIZE
        delay = delay or config.REPORT_DELAY
        
        self.start_time = datetime.now()
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting batch {reason} reporting")
        logger.info(f"Total targets: {len(usernames)}")
        logger.info(f"Batch size: {batch_size}")
        logger.info(f"Delay between reports: {delay}s")
        logger.info(f"{'='*60}\n")
        
        total_batches = (len(usernames) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(usernames))
            batch = usernames[start_idx:end_idx]
            
            logger.info(f"\n{'─'*60}")
            logger.info(f"BATCH {batch_num + 1}/{total_batches}")
            logger.info(f"Processing accounts {start_idx + 1} to {end_idx}")
            logger.info(f"{'─'*60}\n")
            
            for i, username in enumerate(batch, 1):
                logger.info(f"[{start_idx + i}/{len(usernames)}] @{username}")
                
                self.report_with_retry(username, max_retries=config.RETRY_ATTEMPTS, reason=reason)
                
                if i < len(batch):
                    time.sleep(delay)
            
            # Batch delay
            if batch_num < total_batches - 1:
                logger.info(f"\n⏳ Batch complete. Waiting {config.BATCH_DELAY}s before next batch...")
                time.sleep(config.BATCH_DELAY)
        
        self.end_time = datetime.now()
        
        return self.get_statistics()
    
    def get_statistics(self) -> Dict:
        """Get detailed reporting statistics"""
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0
        total = self.reports_sent + self.reports_failed
        
        stats = {
            'summary': {
                'total_reports': total,
                'successful': self.reports_sent,
                'failed': self.reports_failed,
                'success_rate': (self.reports_sent / total * 100) if total > 0 else 0,
                'duration_seconds': duration,
            },
            'successful_reports': self.successful_reports,
            'failed_reports': self.failed_reports,
            'timestamp': datetime.now().isoformat()
        }
        
        return stats
    
    def save_results(self):
        """Save detailed results to files"""
        stats = self.get_statistics()
        
        # Save overall statistics
        with open(config.STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"✓ Statistics saved to {config.STATS_FILE}")
        
        # Save successful reports
        with open(config.SUCCESSFUL_REPORTS_FILE, 'w') as f:
            json.dump(self.successful_reports, f, indent=2)
        logger.info(f"✓ Successful reports saved to {config.SUCCESSFUL_REPORTS_FILE}")
        
        # Save failed reports
        with open(config.FAILED_REPORTS_FILE, 'w') as f:
            json.dump(self.failed_reports, f, indent=2)
        logger.info(f"✓ Failed reports saved to {config.FAILED_REPORTS_FILE}")
    
    def print_summary(self, stats: Dict):
        """Print a formatted summary of results"""
        print(f"""
╔════════════════════════════════════════════════╗
║           REPORTING SUMMARY                    ║
╚════════════════════════════════════════════════╝

Total Reports:        {stats['summary']['total_reports']}
Successful:           {stats['summary']['successful']} ✓
Failed:               {stats['summary']['failed']} ✗
Success Rate:         {stats['summary']['success_rate']:.1f}%
Duration:             {stats['summary']['duration_seconds']:.1f}s

""")
        
        if self.successful_reports:
            print("Successful Accounts:")
            for report in self.successful_reports[:10]:
                print(f"  ✓ @{report['username']}")
            
            if len(self.successful_reports) > 10:
                print(f"  ... and {len(self.successful_reports) - 10} more")
        
        if self.failed_reports:
            print(f"\nFailed Accounts:")
            for report in self.failed_reports[:5]:
                print(f"  ✗ @{report['username']}")
            
            if len(self.failed_reports) > 5:
                print(f"  ... and {len(self.failed_reports) - 5} more")
        
        print(f"\n{'='*44}\n")


def main():
    """Main execution"""
    print("""
    ╔════════════════════════════════════════════════╗
    ║    Advanced Harassment Report Bot v1.0         ║
    ║    With Batching & Retry Logic                ║
    ╚════════════════════════════════════════════════╝
    """)
    
    # Load targets
    reporter = AdvancedHarassmentReporter()
    usernames = reporter.load_targets_from_file(config.TARGETS_FILE)
    
    if not usernames:
        print("\n✗ No targets loaded. Please add usernames to targets.txt")
        return
    
    # Run batch reporting
    try:
        stats = reporter.report_batch(usernames, reason='harassment')
        reporter.save_results()
        reporter.print_summary(stats)
        print(f"✓ Complete! Check logs for details:")
        print(f"  - {config.LOG_FILE}")
        print(f"  - {config.STATS_FILE}")
        print(f"  - {config.SUCCESSFUL_REPORTS_FILE}")
        print(f"  - {config.FAILED_REPORTS_FILE}")
    except KeyboardInterrupt:
        logger.info("\n⚠️  Reporting cancelled by user")
        reporter.save_results()
        print("\n✓ Results saved before exit.")
    except Exception as e:
        logger.error(f"✗ Unexpected error: {str(e)}")
        reporter.save_results()
        print(f"\n✗ Error occurred. Partial results saved.")


if __name__ == '__main__':
    main()
