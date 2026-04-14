# Automation Module

This module contains the Selenium-based automation suite.

## Layout

- `src/pages/` page objects grouped by feature
- `src/config/` shared settings and path resolution
- `src/utils/` helper functions reused across tests
- `tests/` executable test modules
- `data/` local files used for upload-based scenarios
- `screenshots/` output folder for debug artifacts
- `main.py` local launcher for manual execution
- `../tests/` pytest-based coverage for the evolving framework layer

## Run

```bash
python -m tools.automation.main
```

Or run tests through the repository helper:

```bash
bash scripts/dev/run_tests.sh
```

## Configuration

Set `BASE_URL` to point tests at a different environment when needed.

The legacy runnable scripts remain intact, while the repository-level `tests/` folder shows the direction toward a more standard pytest-driven framework.
