# detector.py

import re

from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    "verify",
    "urgent",
    "login",
    "bank",
    "password",
    "click here",
    "security alert",
    "confirm identity",
    "update account"
]

SUSPICIOUS_DOMAINS = [
    ".ru",
    ".xyz",
    ".tk",
    ".gq",
    ".top"
]

URL_REGEX = r"(https?://[^\s]+)"


# -----------------------------
# EXTRACT URLS
# -----------------------------
def extract_urls(text):

    return re.findall(
        URL_REGEX,
        text
    )


# -----------------------------
# ANALYZE EMAIL
# -----------------------------
def analyze_email(subject, sender, body):

    risk_score = 0

    combined_text = f"{subject} {body}".lower()

    urls_detected = []

    # Keyword detection
    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in combined_text:
            risk_score += 10

    # URL detection
    urls = extract_urls(body)

    for url in urls:

        urls_detected.append(url)

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        for bad_domain in SUSPICIOUS_DOMAINS:

            if domain.endswith(bad_domain):
                risk_score += 25

        if len(url) > 75:
            risk_score += 10

    # Sender checks
    if "no-reply" in sender.lower():
        risk_score += 5

    # Final classification
    if risk_score >= 70:
        status = "HIGH RISK"

    elif risk_score >= 40:
        status = "SUSPICIOUS"

    else:
        status = "SAFE"

    return {
        "risk_score": risk_score,
        "status": status,
        "urls_detected": urls_detected
    }