# Instagram Harassment Report Bot

A powerful Python-based mass reporting tool for reporting Instagram accounts engaged in harassment.

## ⚠️ Legal Notice

**Use this tool responsibly and only for legitimate reporting.**

- Report only accounts that genuinely violate Instagram's Community Guidelines
- Do not use for false, malicious, or spam reporting
- Instagram actively detects and penalizes automated false reporting
- You are solely responsible for your actions and any consequences
- The author is not accountable for misuse of this tool

---

## Features

### Basic Bot (`harassment_report_bot.py`)
- ✅ Report individual accounts for harassment
- ✅ Get Instagram user IDs from usernames
- ✅ Load targets from text file
- ✅ Automatic logging and statistics
- ✅ Delays between reports to avoid detection
- ✅ Random user agents and request headers
- ✅ Multiple report reasons (harassment, spam, fake accounts, scams, impersonation)

### Advanced Bot (`advanced_bot.py`)
- ✅ All basic features plus:
- ✅ Batch processing with configurable batch sizes
- ✅ Automatic retry logic for failed reports
- ✅ Detailed statistics and tracking
- ✅ Save results to JSON files
- ✅ Progress tracking
- ✅ Summary reports
- ✅ User caching to reduce API calls

---

## Installation

### Requirements
- Python 3.7+
- pip (Python package manager)
- Internet connection

### Setup

```bash
# Clone the repository
git clone https://github.com/plusmm9/instagram-harassment-report-bot.git
cd instagram-harassment-report-bot

# Install dependencies
pip install -r requirements.txt
```

---

## Quick Start

### 1. Prepare Your Targets

Create or edit `targets.txt` with one Instagram username per line:

```
fake_account_123
spam_bot_456
harassing_user_789
impersonator_000
```

### 2. Run the Bot

**Basic bot:**
```bash
python harassment_report_bot.py
```

**Advanced bot (recommended):**
```bash
python advanced_bot.py
```

### 3. Monitor Progress

Check real-time logs:
```bash
tail -f harassment_reports.log
```

---

## Configuration

Edit `config.py` to customize behavior:

| Setting | Default | Description |
|---------|---------|-------------|
| `REPORT_DELAY` | 2.0s | Delay between individual reports |
| `REPORT_DELAY_JITTER` | 0.5s | Random variation in delay |
| `RETRY_ATTEMPTS` | 3 | Number of retries for failed reports |
| `RETRY_DELAY` | 5s | Delay between retry attempts |
| `BATCH_SIZE` | 50 | Reports to process per batch |
| `BATCH_DELAY` | 300s | Delay between batches (5 minutes) |

---

## Output Files

After running, the bot generates:

- **harassment_reports.log** - Detailed logging of all actions
- **report_stats.json** - Overall statistics
- **successful_reports.json** - Details of successful reports
- **failed_reports.json** - Details of failed reports

### Example Stats Output

```json
{
  "summary": {
    "total_reports": 100,
    "successful": 95,
    "failed": 5,
    "success_rate": 95.0,
    "duration_seconds": 245.5
  },
  "successful_reports": [
    {
      "username": "fake_account_123",
      "user_id": "123456789",
      "timestamp": "2024-01-15T10:30:45.123456",
      "attempt": 1,
      "reason": "harassment"
    }
  ]
}
```

---

## API Reference

### InstagramHarassmentReporter Class

```python
from harassment_report_bot import InstagramHarassmentReporter

# Initialize
reporter = InstagramHarassmentReporter(session_id="your_session_id")

# Report single account
reporter.report_harassment("username")

# Report multiple accounts
reporter.report_multiple(["user1", "user2", "user3"], delay=2.0)

# Load targets from file
usernames = reporter.load_targets_from_file("targets.txt")

# Get user ID
user_id = reporter.get_user_id("username")

# Save statistics
stats = reporter.report_multiple(usernames)
reporter.save_report_stats(stats)
```

### AdvancedHarassmentReporter Class

```python
from advanced_bot import AdvancedHarassmentReporter

# Initialize
reporter = AdvancedHarassmentReporter()

# Report with retry
reporter.report_with_retry("username", max_retries=5)

# Batch reporting
usernames = reporter.load_targets_from_file("targets.txt")
stats = reporter.report_batch(usernames, batch_size=25, delay=2.0)

# Save all results
reporter.save_results()

# Print summary
reporter.print_summary(stats)
```

---

## Report Reasons

Supported report reasons:

| Reason | Code | Description |
|--------|------|-------------|
| `harassment` | 8 | Targeted harassment, bullying |
| `spam` | 3 | Spam content or behavior |
| `fake_account` | 7 | Fake or impersonation account |
| `scam` | 13 | Scam or fraud activity |
| `impersonation` | 6 | Impersonation of person/brand |
| `hate_speech` | 12 | Hate speech or discrimination |

---

## Best Practices

✅ **DO:**
- Report accounts genuinely engaged in harassment
- Use appropriate delays (2-5 seconds) between reports
- Batch reports across multiple runs
- Monitor logs for issues
- Keep targets list organized
- Start with small batches to test

❌ **DON'T:**
- File false or malicious reports
- Report too rapidly (will trigger rate limits)
- Use for competitor sabotage
- Run multiple instances simultaneously
- Ignore Instagram's Community Guidelines
- Reuse targets immediately after reporting

---

## Troubleshooting

### Issue: "Could not find user ID"
**Solution:**
- Check if username exists and is spelled correctly
- Account might be private/deleted
- Try again in a few moments

### Issue: Reports failing
**Solution:**
- Instagram may be rate-limiting your requests
- Increase delays in config.py
- Use advanced_bot.py for automatic retries
- Check your internet connection

### Issue: Bot gets detected/blocked
**Solution:**
- Increase delays between reports
- Use batch mode with longer batch delays
- Limit reports per session
- Use VPN/proxy if IP is flagged

### Issue: Targets file not found
**Solution:**
- Create `targets.txt` in the same directory as the script
- Ensure file is readable and has proper formatting

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Avg Time per Report | 1-3 seconds |
| Success Rate | 85-95% |
| Batch Processing | 50 reports per batch |
| Batch Delay | 5 minutes (recommended) |
| Average Throughput | 1200 reports/hour |

---

## Logging

The bot logs all activity to `harassment_reports.log`:

```
2024-01-15 10:30:45 - INFO - Starting batch harassment reporting
2024-01-15 10:30:46 - INFO - [1/100] @fake_account_123
2024-01-15 10:30:46 - INFO - ✓ Found user ID for @fake_account_123: 123456789
2024-01-15 10:30:47 - INFO - ✓ Successfully reported @fake_account_123 for harassment
2024-01-15 10:30:49 - INFO - [2/100] @spam_bot_456
```

---

## Disclaimer

```
I am not accountable for any of your actions.

This tool is provided for educational and legitimate reporting purposes only.
Misuse of this tool for false reporting, harassment, or malicious campaigns
is prohibited and may result in legal consequences.

Use at your own risk.
```

---

**Made with ❤️ for responsible Instagram reporting**
