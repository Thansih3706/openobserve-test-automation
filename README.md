# OpenObserve Test Automation

This repository contains automated tests for OpenObserve:
- API tests with `pytest` + `allure`
- UI tests with `Playwright`

## Project Layout

```text
src/main/openobserve/
  api_tests/      # Python API tests
  ui-tests/       # Playwright UI tests
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- `pip` and `npm`
- OpenObserve instance running and reachable

## Environment Variables

Use `.env.example` files as templates:

- Root API template: `.env.example`
- UI template: `src/main/openobserve/ui-tests/.env.example`

Required variables:

- API tests: `OO_USERNAME`, `OO_PASSWORD` (optional overrides: `OO_BASE_URL`, `OO_ORG`)
- UI tests: `USERNAME`, `PASSWORD`

## API Tests (Pytest)

1) Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set API env vars (from root):

```bash
cp .env.example .env
# Fill OO_USERNAME and OO_PASSWORD in .env
```

2) Run tests:

```bash
pytest src/main/openobserve/api_tests/tests -v
```

3) Run with Allure output:

```bash
pytest src/main/openobserve/api_tests/tests --alluredir=allure-results -v
allure serve allure-results
```

## UI Tests (Playwright)

1) Install UI dependencies:

```bash
cd src/main/openobserve/ui-tests
npm install
```

2) Configure UI `.env` inside `src/main/openobserve/ui-tests`.

```bash
cp src/main/openobserve/ui-tests/.env.example src/main/openobserve/ui-tests/.env
# Fill USERNAME and PASSWORD in ui-tests/.env
```

3) Run tests:

```bash
npx playwright test
```

## Environment Notes

- API fixtures read credentials from environment variables in `src/main/openobserve/api_tests/conftest.py`.
- UI tests read credentials/settings from `src/main/openobserve/ui-tests/.env`.

## Useful Commands

```bash
# API smoke only
pytest src/main/openobserve/api_tests/tests -m smoke -v

# UI single spec
npx playwright test tests/pipeline.spec.js
```