<<<<<<< HEAD
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
=======
"""Heuristic-based phishing URL detection engine."""

import re
from dataclasses import dataclass, field

import tldextract

from config import (
    MAX_DOMAIN_ENTROPY,
    MAX_SPECIAL_CHAR_RATIO,
    MAX_URL_LENGTH,
    RISK_LEVELS,
    SUSPICIOUS_KEYWORDS,
)
from utils import is_valid_url, normalize_url, parse_url, shannon_entropy, special_char_ratio


@dataclass
class Finding:
    rule: str
    description: str
    score: int


@dataclass
class ScanResult:
    url: str
    threat_score: int
    risk_level: str
    risk_label: str
    risk_color: str
    findings: list[Finding] = field(default_factory=list)
    is_valid: bool = True
    error: str | None = None


def _classify_risk(score: int) -> tuple[str, str, str]:
    for level, meta in RISK_LEVELS.items():
        if meta["min"] <= score <= meta["max"]:
            return level, meta["label"], meta["color"]
    return "critical", RISK_LEVELS["critical"]["label"], RISK_LEVELS["critical"]["color"]


def _check_https(parsed: dict, findings: list[Finding]) -> int:
    if parsed["scheme"] != "https":
        findings.append(
            Finding(
                rule="https",
                description="URL does not use HTTPS encryption",
                score=20,
            )
        )
        return 20
    findings.append(
        Finding(
            rule="https",
            description="URL uses HTTPS",
            score=0,
        )
    )
    return 0


def _check_suspicious_keywords(url_lower: str, findings: list[Finding]) -> int:
    matched = [kw for kw in SUSPICIOUS_KEYWORDS if kw in url_lower]
    if matched:
        score = min(25, 8 + len(matched) * 4)
        findings.append(
            Finding(
                rule="keywords",
                description=f"Suspicious keywords detected: {', '.join(matched[:5])}"
                + ("..." if len(matched) > 5 else ""),
                score=score,
            )
        )
        return score
    return 0


def _check_ip_domain(hostname: str, findings: list[Finding]) -> int:
    ipv4 = re.match(
        r"^(\d{1,3}\.){3}\d{1,3}$",
        hostname.split(":")[0],
    )
    ipv6 = hostname.startswith("[") or "::" in hostname
    if ipv4 or ipv6:
        findings.append(
            Finding(
                rule="ip_domain",
                description="URL uses an IP address instead of a domain name",
                score=25,
            )
        )
        return 25
    return 0


def _check_url_length(full_url: str, findings: list[Finding]) -> int:
    length = len(full_url)
    if length > MAX_URL_LENGTH:
        excess = length - MAX_URL_LENGTH
        score = min(20, 10 + excess // 10)
        findings.append(
            Finding(
                rule="url_length",
                description=f"Unusually long URL ({length} characters)",
                score=score,
            )
        )
        return score
    return 0


def _check_special_chars(full_url: str, findings: list[Finding]) -> int:
    ratio = special_char_ratio(full_url)
    if ratio > MAX_SPECIAL_CHAR_RATIO:
        score = min(15, int(ratio * 80))
        findings.append(
            Finding(
                rule="special_chars",
                description=f"Excessive special characters ({ratio:.0%} of URL)",
                score=score,
            )
        )
        return score
    return 0


def _check_domain_randomness(hostname: str, findings: list[Finding]) -> int:
    if not hostname:
        return 0
    domain_part = hostname.split(":")[0]
    registered = tldextract.extract(domain_part)
    subdomain = registered.subdomain or ""
    domain_name = registered.domain or domain_part

    target = domain_name if domain_name else domain_part
    entropy = shannon_entropy(target)

    has_many_digits = sum(c.isdigit() for c in target) >= len(target) * 0.3
    has_hyphens = target.count("-") >= 2

    score = 0
    reasons = []

    if entropy >= MAX_DOMAIN_ENTROPY:
        score += 12
        reasons.append("high domain randomness")
    if has_many_digits:
        score += 8
        reasons.append("many digits in domain")
    if has_hyphens:
        score += 6
        reasons.append("multiple hyphens in domain")
    if subdomain and len(subdomain) > 20:
        score += 8
        reasons.append("long subdomain")

    if score > 0:
        findings.append(
            Finding(
                rule="domain_randomness",
                description="Suspicious domain pattern: " + ", ".join(reasons),
                score=min(20, score),
            )
        )
        return min(20, score)
    return 0


def _check_at_symbol(full_url: str, findings: list[Finding]) -> int:
    if "@" in full_url:
        findings.append(
            Finding(
                rule="at_symbol",
                description="URL contains '@' which may hide the real destination",
                score=15,
            )
        )
        return 15
    return 0


def _check_double_slash(path: str, findings: list[Finding]) -> int:
    if "//" in path:
        findings.append(
            Finding(
                rule="double_slash",
                description="Double slash in URL path (possible redirect trick)",
                score=10,
            )
        )
        return 10
    return 0


def analyze_url(url: str) -> ScanResult:
    """Run heuristic analysis on a URL and return threat assessment."""
    if not url or not url.strip():
        return ScanResult(
            url=url,
            threat_score=0,
            risk_level="safe",
            risk_label="Safe",
            risk_color=RISK_LEVELS["safe"]["color"],
            is_valid=False,
            error="Please enter a URL to scan.",
        )

    if not is_valid_url(url):
        return ScanResult(
            url=url.strip(),
            threat_score=0,
            risk_level="safe",
            risk_label="Safe",
            risk_color=RISK_LEVELS["safe"]["color"],
            is_valid=False,
            error="Invalid URL format. Please enter a valid link.",
        )

    parsed = parse_url(url)
    findings: list[Finding] = []
    url_lower = parsed["full"].lower()

    total = 0
    total += _check_https(parsed, findings)
    total += _check_suspicious_keywords(url_lower, findings)
    total += _check_ip_domain(parsed["hostname"], findings)
    total += _check_url_length(parsed["full"], findings)
    total += _check_special_chars(parsed["full"], findings)
    total += _check_domain_randomness(parsed["hostname"], findings)
    total += _check_at_symbol(parsed["full"], findings)
    total += _check_double_slash(parsed["path"], findings)

    threat_score = min(100, total)
    risk_level, risk_label, risk_color = _classify_risk(threat_score)

    # Only report findings that contributed risk
    risk_findings = [f for f in findings if f.score > 0]

    return ScanResult(
        url=parsed["original"],
        threat_score=threat_score,
        risk_level=risk_level,
        risk_label=risk_label,
        risk_color=risk_color,
        findings=risk_findings if risk_findings else findings[:1],
        is_valid=True,
    )


def result_to_dict(result: ScanResult) -> dict:
    """Serialize scan result for JSON responses."""
    return {
        "url": result.url,
        "threat_score": result.threat_score,
        "risk_level": result.risk_level,
        "risk_label": result.risk_label,
        "risk_color": result.risk_color,
        "is_valid": result.is_valid,
        "error": result.error,
        "findings": [
            {"rule": f.rule, "description": f.description, "score": f.score}
            for f in result.findings
        ],
    }
>>>>>>> 0de8775522112e69ff8fb73e40bfa04359e84c5c
