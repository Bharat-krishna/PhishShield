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
