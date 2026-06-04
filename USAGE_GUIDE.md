# Instagram Harassment Report Bot - Usage Guide

## Quick Start (2 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Targets
Edit `targets.txt` and add Instagram usernames (one per line):
```
fake_account_123
spam_bot_456
```

### 3. Run Bot
```bash
# Basic bot
python harassment_report_bot.py

# Or advanced bot (recommended)
python advanced_bot.py
```

---

## Detailed Configuration

### File: `config.py`

#### Delays (Avoid Detection)
```python
REPORT_DELAY = 2.0              # Base delay in seconds
REPORT_DELAY_JITTER = 0.5       # Random variation
```
Effect: Creates random delays between 1.5s - 2.5s

#### Batch Settings
```python
BATCH_SIZE = 50                 # Reports per batch
BATCH_DELAY = 300               # Delay between batches (5 min)
```
Effect: Reports in groups of 50, waits 5 minutes between batches

#### Retry Settings
```python
RETRY_ATTEMPTS = 3              # Max retries
RETRY_DELAY = 5                 # Wait between retries (seconds)
```

### Presets

**Fast Mode:**
```python
REPORT_DELAY = 0.5
BATCH_SIZE = 100
BATCH_DELAY = 60
```

**Stealth Mode:**
```python
REPORT_DELAY = 5.0
BATCH_SIZE = 25
BATCH_DELAY = 900  # 15 minutes
```

---

## Output Files

### harassment_reports.log
Detailed activity log:
```
2024-01-15 10:30:46 - INFO - [1/100] @fake_account_123
2024-01-15 10:30:46 - INFO - ✓ Successfully reported @fake_account_123
```

### report_stats.json
Summary statistics:
```json
{
  "summary": {
    "total_reports": 100,
    "successful": 95,
    "failed": 5,
    "success_rate": 95.0,
    "duration_seconds": 245.5
  }
}
```

### successful_reports.json
Details of successful reports

### failed_reports.json
Details of failed reports

---

## Monitoring

### Watch Live Log
```bash
tail -f harassment_reports.log
```

### View Statistics
```bash
cat report_stats.json | jq .summary
```

### Count Results
```bash
jq '.successful_reports | length' successful_reports.json
```

---

## Troubleshooting

### "Could not find user ID"
- Username doesn't exist
- Account is private/deleted
- Try again later

### Reports Failing (429 Error)
- Instagram rate limiting you
- Increase delays in config.py
- Wait 1-2 hours before retrying

### No targets.txt
```bash
echo "username1" > targets.txt
echo "username2" >> targets.txt
```

### Bot Hangs
- Press Ctrl+C to stop
- Check if targets.txt has usernames
- Verify internet connection

---

## Report Reasons

```python
reporter.report_multiple(usernames, reason='harassment')  # Default
reporter.report_multiple(usernames, reason='spam')
reporter.report_multiple(usernames, reason='fake_account')
reporter.report_multiple(usernames, reason='scam')
reporter.report_multiple(usernames, reason='impersonation')
```

---

## API Examples

### Simple Report
```python
from harassment_report_bot import InstagramHarassmentReporter

reporter = InstagramHarassmentReporter()
reporter.report_harassment("username")
```

### Batch Report
```python
usernames = ["user1", "user2", "user3"]
stats = reporter.report_multiple(usernames, delay=2.0)
print(f"Success: {stats['success_rate']:.1f}%")
```

### Advanced with Retries
```python
from advanced_bot import AdvancedHarassmentReporter

reporter = AdvancedHarassmentReporter()
usernames = reporter.load_targets_from_file("targets.txt")
stats = reporter.report_batch(usernames)
reporter.save_results()
```

---

## Version
- **Version:** 1.0
- **Python:** 3.7+
- **Status:** Active

## Disclaimer

Use responsibly. Report only genuine violations of Instagram's Community Guidelines.
