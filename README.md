# OpenObserve Test Automation

This repository contains automated tests for OpenObserve:
- API tests with `pytest` + `allure`
- UI tests with `Playwright`

---

## Test Modules Covered

- **Module 1 – Logs (API)**  
  Ingest logs and verify search results using API.

- **Module 2 – Alerts (UI + API)**  
  Create template, destination, and real-time alert.  
  Trigger alert and verify data is routed to destination stream.

- **Module 3 – Dashboard (UI + API)**  
  Create dashboard and panel based on ingested data.  
  Validate panel displays actual data.

- **Module 4 – Pipeline (UI + API)**  
  Create pipeline connecting source and destination streams.  
  Verify routed data in destination stream.

---

## Project Layout


src/main/openobserve/
api_tests/ # Python API tests
ui-tests/ # Playwright UI tests


---

## Prerequisites

- Python 3.11+
- Node.js 18+
- pip and npm
- OpenObserve instance running at http://localhost:5080

---

## Environment Variables

Use `.env` files as templates:

- API template: `src/main/openobserve/api_tests/.env`
- UI template: `src/main/openobserve/ui-tests/.env`

### Required variables

#### API tests
- `USERNAME`
- `PASSWORD`

#### UI tests
- `USERNAME`
- `PASSWORD`

---

## API Tests (Pytest)

### 1) Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r src/main/openobserve/api_tests/requirements.txt
2) Configure environment
cp src/main/openobserve/api_tests/.env.example src/main/openobserve/api_tests/.env
3) Run tests
pytest src/main/openobserve/api_tests/tests -v
4) Run with Allure report
pytest src/main/openobserve/api_tests/tests --alluredir=allure-results -v
allure serve allure-results


UI Tests (Playwright)
1) Install dependencies
cd src/main/openobserve/ui-tests
npm install
2) Install browsers
npx playwright install
3) Configure environment
cp .env
4) Run tests
npx playwright test
# Run specific UI test
npx playwright test tests/pipeline.spec.js

Execution Recommendation
Run API tests first to validate ingestion and search
Run UI tests after API validation
Key Design Decisions
Used API-based data seeding for reliable test setup
Implemented retry logic for near-real-time systems
Followed Page Object Model (POM) for UI tests
Centralized dynamic test data in helper utilities
Avoided fixed waits; used condition-based waits
Known Limitations
Pipeline canvas uses drag-and-drop interactions
Node connection may be flaky in automation
Data validation is performed via API to ensure correctness