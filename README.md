# 🛡 PhishShield — Real-Time AI Phishing Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge&logo=flask">
  <img src="https://img.shields.io/badge/Cybersecurity-Phishing_Detection-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>

---

# 📌 Overview

PhishShield is a cybersecurity-focused real-time phishing detection platform built using Python Flask.

The system continuously monitors Gmail inbox activity, analyzes incoming emails using heuristic phishing detection techniques, classifies threat levels, and visualizes email security analytics through a modern SOC-style dashboard.

Unlike traditional static URL scanners, PhishShield introduces:

* Real-time inbox monitoring
* Live phishing analysis
* Threat intelligence visualization
* Cyber-themed SOC dashboard
* Dynamic email classification
* Threat analytics graphs

This project was developed for:

* Cybersecurity learning
* Security awareness demonstrations
* Portfolio showcasing
* SOC dashboard simulation
* Phishing analysis research

---

# 🚀 Key Features

## 🔴 Real-Time Gmail Monitoring

PhishShield continuously monitors Gmail inbox activity using IMAP.

### Capabilities

* Live email scanning
* Automatic inbox polling
* Continuous monitoring
* Dynamic dashboard updates
* No manual refresh required

---

## 🛡 Heuristic Phishing Detection Engine

Incoming emails are analyzed using custom heuristic threat intelligence rules.

### Detection Checks

| Detection Technique       | Purpose                            |
| ------------------------- | ---------------------------------- |
| Suspicious keywords       | Detect social engineering attempts |
| Fake login patterns       | Identify credential theft attempts |
| Suspicious TLDs           | Detect malicious domains           |
| Long URLs                 | Detect obfuscation                 |
| Excess special characters | Detect suspicious formatting       |
| URL randomness            | Detect phishing-generated domains  |
| Double slash redirects    | Detect redirect abuse              |
| `@` symbol misuse         | Detect misleading URLs             |
| No-reply sender patterns  | Detect spoofed systems             |

---

## 📊 SOC-Style Cybersecurity Dashboard

The platform includes a professional cyber-themed Security Operations Center (SOC) dashboard.

### Dashboard Features

* Live email feed
* Real-time threat monitoring
* Threat severity badges
* Cyber-themed UI
* Animated cyber cards
* Live threat statistics
* Interactive analytics modal

---

## 📈 Threat Intelligence Analytics

PhishShield includes visual analytics for email security monitoring.

### Analytics Features

* SAFE email count
* SUSPICIOUS email count
* HIGH RISK threat count
* Interactive bar graph visualization
* Real-time statistics updates

---

# 🧠 Threat Classification System

| Risk Score | Classification |
| ---------- | -------------- |
| 0 – 39     | SAFE           |
| 40 – 69    | SUSPICIOUS     |
| 70 – 100   | HIGH RISK      |

---

# ⚙️ Technology Stack

| Technology          | Purpose                 |
| ------------------- | ----------------------- |
| Python 3.10+        | Core backend language   |
| Flask               | Web framework           |
| Gmail IMAP          | Inbox monitoring        |
| HTML/CSS/JavaScript | Frontend UI             |
| Chart.js            | Analytics visualization |
| Threading           | Background monitoring   |
| Heuristic Analysis  | Threat detection        |
| Git/GitHub          | Version control         |

---

# 📂 Project Structure

```text
PhishShield/
│
├── app.py
├── detector.py
├── gmail_scanner.py
├── realtime_monitor.py
├── utils.py
├── config.py
│
├── templates/
│   ├── index.html
│   └── live_email.html
│
├── static/
├── docs/
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

# 🔄 System Workflow

```text
User Login
    ↓
Gmail Inbox Monitoring
    ↓
Email Fetching via IMAP
    ↓
Threat Intelligence Analysis
    ↓
Risk Classification
    ↓
Dashboard Visualization
    ↓
Threat Analytics Graph
```

---

# 🖥 Application Screens

## 1️⃣ Login Interface

The user enters:

* Gmail address
* Google App Password

The monitoring process starts automatically.

---

## 2️⃣ Real-Time Monitoring Dashboard

The dashboard displays:

* Incoming emails
* Sender details
* Email subject
* Email preview
* Threat score
* Threat classification

---

## 3️⃣ Threat Analytics Modal

Clicking:

```text
VIEW THREAT ANALYTICS
```

opens:

* Live bar graph
* Threat counts
* Security statistics

---

# 📦 Installation Guide

## 1️⃣ Clone Repository

```powershell
git clone https://github.com/Bharat-krishna/PhishShield.git
cd PhishShield
```

---

## 2️⃣ Create Virtual Environment

```powershell
python -m venv venv
```

---

## 3️⃣ Activate Environment

### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 5️⃣ Run Application

```powershell
python app.py
```

---

## 6️⃣ Open Browser

```text
http://127.0.0.1:5000
```

---

# 🔐 Gmail Setup Guide

To enable real-time inbox monitoring:

## Step 1 — Enable 2-Step Verification

Go to:

[https://myaccount.google.com/security](https://myaccount.google.com/security)

Enable:

```text
2-Step Verification
```

---

## Step 2 — Generate App Password

Open:

[https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

Generate a:

```text
Mail App Password
```

---

## Step 3 — Login to PhishShield

Use:

* Gmail address
* Generated App Password

⚠ Never use your actual Gmail password.

---

# 🧪 Example Threat Detection

| Email Subject                   | Classification |
| ------------------------------- | -------------- |
| Project Meeting Tomorrow        | SAFE           |
| Verify Your Account Now         | HIGH RISK      |
| Security Alert — Login Required | SUSPICIOUS     |
| Password Expiry Warning         | HIGH RISK      |

---

# 📡 API Endpoints

| Endpoint         | Method | Description                    |
| ---------------- | ------ | ------------------------------ |
| `/`              | GET    | Login interface                |
| `/start-monitor` | POST   | Starts monitoring              |
| `/live`          | GET    | Live dashboard                 |
| `/api/threats`   | GET    | Returns live email threat data |

---

# 📈 Future Improvements

Potential future upgrades:

* Machine learning threat detection
* OCR-based phishing detection
* Attachment scanning
* Email spoofing analysis
* Dark web intelligence integration
* Real-time WebSocket updates
* Multi-user authentication
* Database integration
* Cloud deployment
* SIEM integration

---

# 🔒 Security Notes

* App passwords should never be hardcoded
* Sensitive credentials should be stored in environment variables
* `.gitignore` excludes sensitive files
* This project is educational and not enterprise hardened

---

# ⚠ Disclaimer

PhishShield is intended for:

* Educational use
* Cybersecurity demonstrations
* Portfolio projects
* Research purposes

This project uses heuristic analysis and does not guarantee complete malware or phishing detection accuracy.

Do not rely on this system as a sole enterprise security solution.

---

# 👨‍💻 Developer

## Bharat Krishna

Cybersecurity & Web Development Enthusiast

### GitHub Repository

[https://github.com/Bharat-krishna/PhishShield](https://github.com/Bharat-krishna/PhishShield)

---

# 📄 License

This project is licensed under the MIT License.

See the LICENSE file for details.
