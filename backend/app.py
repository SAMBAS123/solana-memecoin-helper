import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from holder_scanner import scan_holders
from bundle_checker import check_bundle
from liquidity_alert import monitor_liquidity_poll
from notify import send_telegram_message
import time
import requests
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r\"/*\": {\"origins\": [\"http://127.0.0.1\", \"http://127.0.0.1:*\", \"null\"]}})
active_monitors = {}
recent_alerts = []
MAX_ALERTS = 100
TELEGRAM_BOT_TOKEN = os.getenv(\"TELEGRAM_BOT_TOKEN\")
def tg_poller():
    update_id = 0
    while True:
        try:
            resp = requests.get(f\"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={update_id + 1}\")
            data = resp.json()
            if data[\"ok\"]:
                for update in data[\"result\"]:
                    update_id = update[\"update_id\"]
                    if \"message\" in update and \"text\" in update[\"message\"]:
                        text = update[\"message\"][\"text\"]
                        chat_id = update[\"message\"][\"chat\"][\"id\"]
                        if text.startswith(\"scan \"):
                            token = text.split(\"scan \")[1].strip()
                            holders = scan_holders(token)
                            send_telegram_message(reply, chat_id=chat_id)
        except Exception:
            pass
        time.sleep(10)
threading.Thread(target=tg_poller, daemon=True).start()
@app.get(\"/health\")
def health():
    return {\"ok\": True}
@app.post(\"/scan\")
def scan():
    body = request.get_json(force=True)
    token = (body.get(\"token\") or \"\").strip()
    limit = int(body.get(\"limit\", 10))
    sol_threshold = float(body.get(\"sol_threshold\", 100))
    result = scan_holders(token, holder_limit=limit, sol_threshold=sol_threshold)
    return jsonify({\"token\": token, \"holders\": result})
@app.get(\"/bundle/<bundle_id>\")
def bundle(bundle_id: str):
    result = check_bundle(bundle_id)
    return jsonify(result), (200 if result.get(\"ok\") else 502)
@app.post(\"/monitor/start\")
def monitor_start():
    body = request.get_json(force=True)
    token = (body.get(\"token\") or \"\").strip()
    threshold_pct = float(body.get(\"threshold_pct\", 10))
    interval = int(body.get(\"interval_sec\", 60))
    if not token:
        return jsonify({\"ok\": False, \"error\": \"token required\"}), 400
    if token in active_monitors:
        return jsonify({\"ok\": True, \"message\": \"already monitoring\"})
    stop_flag = {\"stop\": False}
    def should_stop():
        return stop_flag[\"stop\"]
    def on_alert(payload):
        print(f\"[ALERT] {payload}\")
        recent_alerts.append(payload)
        if len(recent_alerts) > MAX_ALERTS:
            del recent_alerts[: len(recent_alerts) - MAX_ALERTS]
        try:
            send_telegram_message(f\"Liquidity alert for {payload.get('token')}: current={payload.get('current_liquidity')} peak={payload.get('peak_liquidity')} threshold={payload.get('threshold_pct')}%\")
        except Exception:
            pass
    thread = threading.Thread(
        target=monitor_liquidity_poll,
        args=(token, threshold_pct, interval, on_alert, should_stop),
        daemon=True,
    )
    thread.start()
    active_monitors[token] = {\"thread\": thread, \"stop_flag\": stop_flag}
    return jsonify({\"ok\": True, \"token\": token})
@app.post(\"/monitor/stop\")
def monitor_stop():
    body = request.get_json(force=True)
    token = (body.get(\"token\") or \"\").strip()
    if token in active_monitors:
        active_monitors[token][\"stop_flag\"][\"stop\"] = True
        return jsonify({\"ok\": True})
    return jsonify({\"ok\": False, \"error\": \"not monitoring\"}), 404
@app.get(\"/alerts\")
def get_alerts():
    return jsonify({\"alerts\": recent_alerts[-MAX_ALERTS:]})
@app.get(\"/test_alert\")
def test_alert():
    try:
        send_telegram_message(\"Test alert from Solana Memecoin Helper! The app is running.\")
        return jsonify({\"ok\": True, \"message\": \"Test alert sent\"})
    except Exception as e:
        return jsonify({\"ok\": False, \"error\": str(e)}), 500
if __name__ == \"__main__\":
    app.run(host=\"127.0.0.1\", port=5000, debug=False, use_reloader=False)
