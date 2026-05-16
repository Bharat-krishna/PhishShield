# PhishShield — Architecture

This document describes how PhishShield is structured, how data flows through the system, and how to extend the detection engine.

---

## Design goals

1. **Modularity** — detection logic is separate from HTTP handling and UI
2. **Transparency** — every score has a human-readable reason
3. **Simplicity** — no database required for v1; easy to run locally
4. **Extensibility** — new rules can be added as functions in `detector.py`

---

## Layered architecture

```
┌─────────────────────────────────────────────────────────┐
│  Presentation (templates/, static/)                     │
│  - index.html, style.css, script.js                     │
└──────────────────────────┬──────────────────────────────┘
                           │ fetch POST /api/scan
┌──────────────────────────▼──────────────────────────────┐
│  Application (app.py)                                   │
│  - Routes, request parsing, history storage             │
└──────────────────────────┬──────────────────────────────┘
                           │ analyze_url()
┌──────────────────────────▼──────────────────────────────┐
│  Detection (detector.py)                                │
│  - Heuristic rules, scoring, risk classification        │
└──────────────────────────┬──────────────────────────────┘
                           │ parse_url(), is_valid_url()
┌──────────────────────────▼──────────────────────────────┐
│  Utilities (utils.py) + Configuration (config.py)       │
└─────────────────────────────────────────────────────────┘
```

---

## Core data structures

### `Finding` (detector.py)

Represents one rule outcome:

| Field | Type | Description |
|-------|------|-------------|
| `rule` | `str` | Machine-readable rule ID (e.g. `https`, `keywords`) |
| `description` | `str` | User-facing explanation |
| `score` | `int` | Points added to threat score (0 if informational only) |

### `ScanResult` (detector.py)

Complete analysis output:

| Field | Type | Description |
|-------|------|-------------|
| `url` | `str` | Original user input (trimmed) |
| `threat_score` | `int` | 0–100 aggregated score |
| `risk_level` | `str` | `safe`, `low`, `medium`, `high`, `critical` |
| `risk_label` | `str` | Display label |
| `risk_color` | `str` | Hex color for UI |
| `findings` | `list[Finding]` | Triggered rules (risk-only in response) |
| `is_valid` | `bool` | Whether URL passed validation |
| `error` | `str \| None` | Error message if invalid |

---

## Detection pipeline

`analyze_url(url)` executes in this order:

1. **Empty check** — return error if blank
2. **Validation** — `utils.is_valid_url()` using `validators` library
3. **Parse** — `utils.parse_url()` → scheme, hostname, path, full URL
4. **Rule execution** — each `_check_*` function appends findings and returns score
5. **Aggregation** — `threat_score = min(100, sum(rule_scores))`
6. **Classification** — `_classify_risk()` maps score to `RISK_LEVELS` in config
7. **Filter findings** — only findings with `score > 0` returned (unless all clean)

### Rule function pattern

Each checker follows this contract:

```python
def _check_example(parsed_or_url, findings: list[Finding]) -> int:
    if suspicious_condition:
        findings.append(Finding(rule="...", description="...", score=N))
        return N
    return 0
```

To add a new rule:

1. Implement `_check_your_rule()` in `detector.py`
2. Call it inside `analyze_url()` and add to `total`
3. Optionally add thresholds to `config.py`
4. Document in README detection table

---

## URL utilities (utils.py)

| Function | Purpose |
|----------|---------|
| `normalize_url(url)` | Prepends `http://` if no scheme |
| `is_valid_url(url)` | Boolean validation via `validators.url()` |
| `parse_url(url)` | Returns dict with scheme, hostname, path, netloc |
| `shannon_entropy(text)` | Measures randomness of domain labels |
| `special_char_ratio(text)` | Ratio of unusual characters for obfuscation check |

---

## Application layer (app.py)

### In-memory history

- Global list `recent_scans`
- `_record_scan()` prepends valid results, trims to `RECENT_SCANS_LIMIT`
- **Not thread-safe for high concurrency** — acceptable for demo; use Redis/DB in production

### Routes

| Route | Method | Handler behavior |
|-------|--------|------------------|
| `/` | GET | `render_template("index.html")` |
| `/api/scan` | POST | JSON or form `url` → `analyze_url` → JSON |
| `/api/history` | GET | Returns `{"scans": [...]}` |

---

## Frontend (static/script.js)

- Submits scan via `fetch("/api/scan", { method: "POST", body: JSON })`
- Updates SVG score ring using stroke dashoffset
- Loads history on page load and after each scan
- Clicking a history item re-renders that result in the main panel

No build step or bundler — plain ES6 in the browser.

---

## Security considerations

| Topic | Current behavior | Recommendation for production |
|-------|------------------|-------------------------------|
| SSRF | Does not fetch URLs | Keep it that way unless sandboxed |
| Input size | No explicit limit | Add max URL length at API layer |
| Rate limiting | None | Add per-IP limits |
| CORS | Same-origin default | Configure if API is public |
| Secrets | None required | Use env vars for any API keys later |

---

## Extension points

| Goal | Where to change |
|------|-----------------|
| New detection rule | `detector.py` + `config.py` |
| Risk thresholds | `config.RISK_LEVELS` |
| More keywords | `config.SUSPICIOUS_KEYWORDS` |
| Persistent history | Replace list in `app.py` with SQLite/PostgreSQL |
| Auth for API | Flask middleware or API key header check |
| ML model | New module `ml_detector.py`, call from `analyze_url()` |

---

## Testing suggestions

Manual test matrix:

1. Valid HTTPS domain — expect low score
2. HTTP + IP + keywords — expect high score
3. Empty string — `is_valid: false`
4. `javascript:alert(1)` — should fail validation
5. Very long URL (>200 chars) — length + possible special chars

Automated tests (future): pytest on `analyze_url()` with parametrized URLs.
