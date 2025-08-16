from flask import Flask, jsonify
from dotenv import load_dotenv
import threading
import time
import os

from scanner import fast_memecoin_scan, quick_scan
from trending import get_trending_coins
from log import log_hit

load_dotenv()

app = Flask(__name__)

@app.route('/fast_scan/<token>')
def fast_scan(token):
    result = fast_memecoin_scan(token)
    return jsonify(result)

@app.route('/quickscan/<token>')
def quickscan(token):
    result = quick_scan(token)
    return jsonify(result)

def active_scanner():
    while True:
        coins = get_trending_coins()
        if 'error' not in coins:
            for coin in coins:
                scan = quick_scan(coin['address'])
                if scan['risk_score'] < 50:
                    send_alert(f"Suggest buy: {coin['name']} – Stable liq, low whales (Risk: {scan['risk_score']})")
                    log_hit(coin['address'], scan)
        time.sleep(int(os.getenv('SCAN_INTERVAL', 300)))

if __name__ == '__main__':
    threading.Thread(target=active_scanner, daemon=True).start()
    app.run(debug=True)
