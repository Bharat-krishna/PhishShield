# PhishShield

Lightweight **phishing URL detection** web app using **Python Flask** and heuristic threat scoring (no ML or external APIs).

**Project integrated with AI**

---

## What it does

Analyzes URLs for suspicious patterns, returns a **0–100 threat score**, **risk level** (Safe → Critical), and **reason-based findings**.

| Checks | |
|--------|--|
| HTTPS | Suspicious keywords |
| IP-based hosts | Long / obfuscated URLs |
| Special characters | Domain randomness |
| `@` symbol | Double-slash paths |

---

## Tech stack

Python 3.10+ · Flask · HTML/CSS/JS · `validators` · `tldextract`

---

## Quick start

```powershell
git clone https://github.com/Bharat-krishna/PhishShield.git
cd PhishShield
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**

---

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scan` | POST | `{"url": "https://example.com"}` → threat score + findings |
| `/api/history` | GET | Last 10 scans (in-memory) |

---

## Risk levels

| Score | Level |
|-------|-------|
| 0–24 | Safe |
| 25–44 | Low |
| 45–64 | Medium |
| 65–84 | High |
| 85–100 | Critical |

---

## Project structure

```
app.py          Flask routes
detector.py     Heuristic engine
utils.py        URL validation & parsing
config.py       Keywords & thresholds
templates/      index.html
static/         style.css, script.js
docs/           ARCHITECTURE.md, API.md
```

---

## Disclaimer

Educational tool only — pattern matching, not confirmed malware detection. Do not use as sole security control.

---

## License

[MIT License](LICENSE)

**Repo:** [github.com/Bharat-krishna/PhishShield](https://github.com/Bharat-krishna/PhishShield)
