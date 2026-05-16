"""Utility helpers for PhishShield."""

import math
import re
from collections import Counter
from urllib.parse import urlparse

import validators


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
    return bool(validators.url(normalize_url(url)))


def parse_url(url: str) -> dict:
    """Parse URL into components."""
    normalized = normalize_url(url)
    parsed = urlparse(normalized)
    return {
        "original": url.strip(),
        "normalized": normalized,
        "scheme": (parsed.scheme or "").lower(),
        "netloc": parsed.netloc.lower(),
        "hostname": parsed.hostname.lower() if parsed.hostname else "",
        "path": parsed.path or "",
        "full": normalized,
    }


def shannon_entropy(text: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not text:
        return 0.0
    counts = Counter(text)
    length = len(text)
    return -sum(
        (count / length) * math.log2(count / length) for count in counts.values()
    )


def count_special_chars(text: str) -> int:
    """Count non-alphanumeric characters (excluding common URL chars)."""
    return len(re.findall(r"[^a-zA-Z0-9.\-_/]", text))


def special_char_ratio(text: str) -> float:
    """Ratio of special characters in text."""
    if not text:
        return 0.0
    return count_special_chars(text) / len(text)
