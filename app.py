<<<<<<< HEAD
# app.py

from flask import Flask, render_template, request, jsonify
from threading import Thread

from realtime_monitor import start_monitor

app = Flask(__name__)

# Store live email scan results
email_logs = []


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# LIVE DASHBOARD
# -----------------------------
@app.route("/live")
def live_dashboard():
    return render_template("live_email.html")


# -----------------------------
# API - SEND EMAIL DATA
# -----------------------------
@app.route("/api/threats")
def get_threats():
    return jsonify(email_logs)


# -----------------------------
# START MONITORING
# -----------------------------
@app.route("/start-monitor", methods=["POST"])
def start_monitoring():

    email_user = request.form["email"]
    email_pass = request.form["password"]

    monitor_thread = Thread(
        target=start_monitor,
        args=(email_user, email_pass, email_logs)
    )

    monitor_thread.daemon = True
    monitor_thread.start()

    return render_template("live_email.html")


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
=======
"""PhishShield - Phishing URL Detection Web Application."""

from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

from config import RECENT_SCANS_LIMIT
from detector import analyze_url, result_to_dict

app = Flask(__name__)
recent_scans: list[dict] = []


def _record_scan(result: dict) -> None:
    if not result.get("is_valid"):
        return
    entry = {
        **result,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
    }
    recent_scans.insert(0, entry)
    del recent_scans[RECENT_SCANS_LIMIT:]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or request.form.get("url") or "").strip()
    result = analyze_url(url)
    payload = result_to_dict(result)
    _record_scan(payload)
    return jsonify(payload)


@app.route("/api/history", methods=["GET"])
def history():
    return jsonify({"scans": recent_scans})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
>>>>>>> 0de8775522112e69ff8fb73e40bfa04359e84c5c
