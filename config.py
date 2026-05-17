"""PhishShield configuration."""

MAX_URL_LENGTH = 75
MAX_SPECIAL_CHAR_RATIO = 0.15
MAX_DOMAIN_ENTROPY = 4.2
RECENT_SCANS_LIMIT = 10
EMAIL_USER = "yourgmail@gmail.com"
EMAIL_PASS = "your_16_char_app_password"

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "account",
    "update",
    "banking",
    "password",
    "confirm",
    "wallet",
    "signin",
    "suspend",
    "urgent",
    "credential",
    "paypal",
    "amazon",
    "microsoft",
    "appleid",
    "free",
    "winner",
    "claim",
    "refund",
    "invoice",
    "billing",
]

RISK_LEVELS = {
    "safe": {"min": 0, "max": 24, "label": "Safe", "color": "#22c55e"},
    "low": {"min": 25, "max": 44, "label": "Low Risk", "color": "#84cc16"},
    "medium": {"min": 45, "max": 64, "label": "Medium Risk", "color": "#f59e0b"},
    "high": {"min": 65, "max": 84, "label": "High Risk", "color": "#f97316"},
    "critical": {"min": 85, "max": 100, "label": "Critical", "color": "#ef4444"},
}
