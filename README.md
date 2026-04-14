# copychecker-selenium-automation

Public Selenium automation portfolio project focused on web flows around file tools such as PDF conversion, image processing, OCR, and plagiarism-related checks.

## Why This Project

This repository shows practical UI automation work in a way that is easy to review:

- Python + Selenium WebDriver
- Page Object Model structure
- reusable file-based test data
- centralized runtime configuration
- interactive local launcher for demos
- lightweight GitHub Actions quality checks

## Project Structure

- `tools/automation/src/pages/` page objects grouped by feature
- `tools/automation/src/config/` shared runtime settings
- `tools/automation/src/utils/` helper functions reused across tests
- `tools/automation/tests/` runnable test modules
- `tools/automation/data/` sample files used by upload workflows
- `tools/automation/main.py` interactive runner
- `scripts/dev/run_tests.sh` helper to run one or many modules
- `.github/workflows/python-checks.yml` CI validation

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional environment variables are listed in [`.env.example`](/Users/kite/copychecker/copychecker-selenium-automation/.env.example).

## Run The Suite

Interactive menu:

```bash
python -m tools.automation.main
```

Run all test modules:

```bash
bash scripts/dev/run_tests.sh
```

Run a single test module:

```bash
bash scripts/dev/run_tests.sh tools/automation/tests/test_pdf_to_text.py
```

## Configuration

This repository is safe to share publicly:

- `BASE_URL` controls which environment the tests target
- local file paths resolve from repository test data where possible
- email credentials are read from environment variables instead of hardcoded values

## Notes For Reviewers

- These tests target live web flows, so site changes can affect results.
- The current CI job performs fast quality checks only. It does not run browser sessions in GitHub-hosted runners yet.
- This codebase is positioned as a solid Selenium foundation that can evolve into a fuller framework.

## Roadmap

1. Add CI/CD execution for selected browser tests
2. Standardize the Page Object Model layer further
3. Introduce Playwright and migrate critical paths gradually
4. Add better assertions, reporting, and environment profiles
