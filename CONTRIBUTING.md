# Contributing to PhishShield

Thank you for your interest in improving PhishShield. This project is designed for learning and portfolio use.

## Getting started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a virtual environment and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app: `python app.py`
5. Create a branch: `git checkout -b feature/your-feature-name`

## What to contribute

- New heuristic detection rules in `detector.py`
- Threshold tuning in `config.py` (with justification in PR description)
- UI/UX improvements in `templates/` and `static/`
- Automated tests (pytest)
- Documentation updates in `README.md` or `docs/`
- Bug fixes with clear reproduction steps

## Code guidelines

- Match existing style: type hints, dataclasses, small focused functions
- Add new configurable values to `config.py`, not hardcoded in rules
- Each detection rule should return a `Finding` with a clear `description`
- Update README detection table when adding rules
- Do not commit `venv/`, `.env`, or secrets

## Pull request checklist

- [ ] Code runs locally without errors
- [ ] README or `docs/` updated if behavior changes
- [ ] Example URLs tested manually
- [ ] No unrelated refactors in the same PR

## Reporting issues

Include:

- URL tested (redact sensitive parts if needed)
- Expected vs actual threat score
- Python version and OS

## Questions

Open a GitHub issue for discussion before large architectural changes (e.g. database, ML integration).
