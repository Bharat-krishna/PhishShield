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