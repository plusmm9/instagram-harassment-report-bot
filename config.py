"""
Configuration settings for Instagram Harassment Report Bot
"""

# Reporting settings
REPORT_DELAY = 2.0  # Seconds between reports (use random jitter)
REPORT_DELAY_JITTER = 0.5  # Random variation in delay

# Request settings
REQUEST_TIMEOUT = 15  # Seconds
RETRY_ATTEMPTS = 3  # Number of retries for failed reports
RETRY_DELAY = 5  # Seconds between retries

# Report reason (harassment = 8)
REPORT_REASON_ID = '8'  # Harassment

# Logging
LOG_FILE = 'harassment_reports.log'
STATS_FILE = 'report_stats.json'

# File paths
TARGETS_FILE = 'targets.txt'
SUCCESSFUL_REPORTS_FILE = 'successful_reports.json'
FAILED_REPORTS_FILE = 'failed_reports.json'

# User agent settings
USE_RANDOM_USER_AGENT = True

# Rate limiting to avoid detection
MIN_DELAY_BETWEEN_REPORTS = 1.5  # Minimum delay in seconds
MAX_DELAY_BETWEEN_REPORTS = 4.0  # Maximum delay in seconds

# Batch reporting settings
BATCH_SIZE = 50  # Reports per batch
BATCH_DELAY = 300  # Delay between batches in seconds (5 minutes)

# Console output
SHOW_BANNER = True
DETAILED_LOGGING = False
