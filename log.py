import csv
import time
import os

LOG_FILE = 'scan_logs.csv'

def log_hit(token, scan_result):
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['token', 'risk_score', 'alpha', 'timestamp'])
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([token, scan_result['risk_score'], scan_result.get('gmgn', {}).get('alpha', ''), time.time()])
