"""Utility helpers for PhishShield."""

import math
import re
from collections import Counter
from urllib.parse import urlparse

import validators

# =========================
# EMAIL PARSER IMPORTS
# =========================

from email import policy
from email.parser import BytesParser


# =========================
# URL HELPERS
# =========================

def normalize_url(url: str) -> str:
    """Ensure URL has a scheme for parsing."""
    url = url.strip()

    if not url:
        return url

    if not re.match(r"^https?://", url, re.IGNORECASE):
        return f"http://{url}"

    return url


def is_valid_url(url: str) -> bool:
    """Check whether the input is a valid URL."""
    return bool(
        validators.url(
            normalize_url(url)
        )
    )


def parse_url(url: str) -> dict:
    """Parse URL into components."""

    normalized = normalize_url(url)

    parsed = urlparse(normalized)

    return {
        "original": url.strip(),
        "normalized": normalized,
        "scheme": (parsed.scheme or "").lower(),
        "netloc": parsed.netloc.lower(),
        "hostname": parsed.hostname.lower()
        if parsed.hostname else "",
        "path": parsed.path or "",
        "full": normalized,
    }


# =========================
# ENTROPY + CHARACTER CHECKS
# =========================

def shannon_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string."""

    if not text:
        return 0.0

    counts = Counter(text)

    length = len(text)

    return -sum(
        (count / length) * math.log2(count / length)
        for count in counts.values()
    )


def count_special_chars(text: str) -> int:
    """Count non-alphanumeric characters."""

    return len(
        re.findall(
            r"[^a-zA-Z0-9.\-_/]",
            text
        )
    )


def special_char_ratio(text: str) -> float:
    """Ratio of special characters in text."""

    if not text:
        return 0.0

    return count_special_chars(text) / len(text)


# =========================
# EMAIL UTILITIES
# =========================

def extract_urls_from_text(text: str) -> list:
    """Extract URLs from arbitrary text."""

    if not text:
        return []

    return re.findall(
        r"https?://[^\s]+",
        text
    )


def parse_eml(file) -> dict:
    """
    Parse uploaded .eml email file.
    Extract sender, subject, body and URLs.
    """

    msg = BytesParser(
        policy=policy.default
    ).parse(file)

    sender = msg.get("from", "")

    subject = msg.get("subject", "")

    body = ""

    # Multipart email
    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()

            if content_type == "text/plain":

                try:
                    body += part.get_content()

                except Exception:
                    continue

    # Single-part email
    else:

        try:
            body = msg.get_content()

        except Exception:
            body = ""

    # Extract URLs
    urls = extract_urls_from_text(body)

    parsed_urls = []

    for url in urls:

        if is_valid_url(url):

            parsed_urls.append(
                parse_url(url)
            )

    return {
        "sender": sender,
        "subject": subject,
        "body": body,
        "urls": parsed_urls,
    }