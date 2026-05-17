# PhishShield — API Specification

Base URL (local development): `http://127.0.0.1:5000`

All API responses use `Content-Type: application/json`.

---

## Authentication

None in v1. All endpoints are public.

---

## Endpoints

### `GET /`

Serves the PhishShield web interface (HTML).

**Response:** `text/html`

---

### `POST /api/scan`

Analyzes a single URL and returns threat assessment.

#### Request

**Headers (recommended):**

```
Content-Type: application/json
```

**Body (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | Yes | URL to analyze |

**Example:**

```http
POST /api/scan HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json

{
  "url": "http://192.168.1.1/login-verify"
}
```

**Alternative:** `application/x-www-form-urlencoded` with field `url`.

#### Response `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | Submitted URL (normalized display uses original trim) |
| `threat_score` | integer | 0–100 |
| `risk_level` | string | `safe` \| `low` \| `medium` \| `high` \| `critical` |
| `risk_label` | string | Human-readable risk name |
| `risk_color` | string | Hex color for UI badges |
| `is_valid` | boolean | `true` if URL format is valid |
| `error` | string \| null | Error message when `is_valid` is false |
| `findings` | array | List of finding objects |

**Finding object:**

| Field | Type | Description |
|-------|------|-------------|
| `rule` | string | Rule identifier |
| `description` | string | Explanation text |
| `score` | integer | Points contributed |

**Example — high risk:**

```json
{
  "url": "http://192.168.1.1/login-verify",
  "threat_score": 53,
  "risk_level": "medium",
  "risk_label": "Medium Risk",
  "risk_color": "#f59e0b",
  "is_valid": true,
  "error": null,
  "findings": [
    {
      "rule": "https",
      "description": "URL does not use HTTPS encryption",
      "score": 20
    },
    {
      "rule": "keywords",
      "description": "Suspicious keywords detected: login, verify",
      "score": 16
    },
    {
      "rule": "ip_domain",
      "description": "URL uses an IP address instead of a domain name",
      "score": 25
    }
  ]
}
```

**Example — invalid URL:**

```json
{
  "url": "not-a-valid-url",
  "threat_score": 0,
  "risk_level": "safe",
  "risk_label": "Safe",
  "risk_color": "#22c55e",
  "is_valid": false,
  "error": "Invalid URL format. Please enter a valid link.",
  "findings": []
}
```

**Example — empty input:**

```json
{
  "url": "",
  "threat_score": 0,
  "risk_level": "safe",
  "risk_label": "Safe",
  "risk_color": "#22c55e",
  "is_valid": false,
  "error": "Please enter a URL to scan.",
  "findings": []
}
```

#### Side effects

If `is_valid` is `true`, the result is added to server-side scan history (max 10 entries).

#### cURL examples

```bash
# JSON request
curl -X POST http://127.0.0.1:5000/api/scan \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://www.example.com\"}"

# Form request
curl -X POST http://127.0.0.1:5000/api/scan \
  -d "url=https://www.example.com"
```

#### PowerShell example

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/scan" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"url":"https://example.com"}'
```

---

### `GET /api/history`

Returns recent scan results stored in server memory.

#### Response `200 OK`

| Field | Type | Description |
|-------|------|-------------|
| `scans` | array | Newest first, up to 10 items |

Each scan object includes all fields from `/api/scan` plus:

| Field | Type | Description |
|-------|------|-------------|
| `scanned_at` | string | ISO 8601 UTC timestamp |

**Example:**

```json
{
  "scans": [
    {
      "url": "https://example.com",
      "threat_score": 0,
      "risk_level": "safe",
      "risk_label": "Safe",
      "risk_color": "#22c55e",
      "is_valid": true,
      "error": null,
      "findings": [],
      "scanned_at": "2026-05-17T14:30:00.123456+00:00"
    }
  ]
}
```

**Note:** History is cleared when the Flask process restarts.

#### cURL example

```bash
curl http://127.0.0.1:5000/api/history
```

---

## Error handling

| Scenario | HTTP status | `is_valid` | `error` |
|----------|-------------|------------|---------|
| Malformed JSON body | 200* | may be false | empty URL error |
| Missing `url` field | 200 | false | "Please enter a URL to scan." |
| Invalid URL string | 200 | false | "Invalid URL format..." |

\* Flask returns 200 with error payload; clients should check `is_valid`.

---

## Rate limits

None in v1. Implement reverse-proxy or Flask-Limiter for public deployments.

---

## Versioning

No API version prefix in v1. Future breaking changes may use `/api/v2/scan`.
