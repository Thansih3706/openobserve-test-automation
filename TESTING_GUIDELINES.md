## Aquanow RFQ API — Automation Testing Guidelines

These guidelines are tailored to the AquaNow RFQ API test automation project. Follow them to keep tests reliable, maintainable, and well-documented.

## Purpose & scope
- Provide automated API coverage for RFQ trade endpoints (quote retrieval, creation, execution, expiration).
- Validate business rules, happy paths, edge cases, and error handling.
- Ensure tests run deterministically with rich reporting (Allure).
- Make it easy for contributors to add, run, and debug tests locally and in CI.

## Project-specific notes
- **Test location**: Tests live under `src/test/aquanow/tests` (configured in `pytest.ini`).
- **Fixtures & configuration**: Global fixtures and environment loading in `conftest.py`.
- **Test data**: Test data and payloads in `resources/testdata/rfq_test_data.py`.
- **Test runners**: `run_suites.py` and `test_runner.py` manage Allure artifact generation, history, and HTML report creation.
- **Base class**: `BaseAPITest` (in `src/main/aquanow/utils/base_test.py`) provides common API testing utilities and assertion helpers.
- **Available markers** (see `pytest.ini`): `smoke` (critical happy-path), `regression` (broader lifecycle), `negative` (failure paths), `rfq` (RFQ-specific tests).

## Test types & where to place them
- **Smoke tests**: Critical happy-path scenarios for RFQ operations. Marked with `@pytest.mark.smoke`. Examples: getting a quote, creating a quote.
- **Regression tests**: Broader business-rule validation and lifecycle tests. Marked with `@pytest.mark.regression`. Examples: quote precedence rules, expired quote behavior.
- **Negative tests**: Invalid input and failure-path tests. Marked with `@pytest.mark.negative`. Examples: missing required fields, invalid ticker format, unauthorized access.
- **RFQ-specific tests**: All tests related to RFQ trade operations. Marked with `@pytest.mark.rfq`. (Orthogonal to smoke/regression/negative.)
- All test files live in `src/test/aquanow/tests/test_*.py`.

## Naming conventions
- **Test files**: `test_*.py` (e.g., `test_rfq_quote.py`, `test_rfq_execute.py`).
- **Test classes**: `Test<Feature>` (e.g., `TestRFQQuote`, `TestRFQExecute`). Inherit from `BaseAPITest` to reuse assertion helpers.
- **Test methods**: `test_<action>_<expected>` (descriptive but concise). Use parameterization for table-driven tests instead of duplicating similar tests.
- **Fixtures**: lower_snake_case names, describe purpose (e.g., `client`, `settings`, `rfq_payload`, `payload_builder`).
- **Test data**: Define static test cases in `resources/testdata/rfq_test_data.py` with clear `id`, `title`, `payload_overrides`, and `expected` fields.

## Fixtures & environment
- **Scope guidance**: 
  - `session` for expensive, reusable resources (e.g., `client`, `settings`).
  - `function` for fixtures that need fresh state per test (e.g., `rfq_payload`).
  - Avoid `autouse=True` unless absolutely necessary.
- **Configuration**: Load environment and settings in `conftest.py`. The `settings` fixture reads from `.env` (or CI variables) for `API_KEY`, `API_SECRET`, `ACCOUNT_ID`, `BASE_URL`, etc.
- **Client fixture**: `AquanowClient` (session-scoped) is pre-configured and reused across tests for efficiency.
- **Payload fixtures**: Use `payload_builder` factory fixture to generate test payloads with overrides. This avoids duplication when multiple similar test cases exist.
- **Base class utilities**: Tests inherit from `BaseAPITest` to use common helpers like `record_api_call()` and `assert_status_code()`.

## Test data & assets
- **Test data location**: `resources/testdata/rfq_test_data.py` — define test case matrices here (positive, negative, edge cases).
- **Payload structure**: Each test case includes:
  - `id`: Unique identifier (used in test parameterization).
  - `title`: Human-readable test description.
  - `payload_overrides`: Dict of fields to override in the base payload.
  - `expected`: Dict of expected values in the response.
- **Example**:
  ```python
  CREATE_QUOTE_POSITIVE_CASES = [
      {
          "id": "buy_deliver_quantity",
          "title": "Create quote with BUY + deliverQuantity",
          "payload_overrides": {"tradeSide": "buy", "deliverQuantity": "100"},
          "expected": {"symbol": "BTCUSD", "side": "BUY", "deliverCurrency": "USD"}
      },
      ...
  ]
  ```
- **Keep test data clean**: Use placeholders (e.g., `BTC-USD` as a standard ticker, `settings.account_id` for account).

## Running tests locally
Below are two recommended ways to run tests locally: (A) the repository helper (`run_suites.py` / `test_runner.py`) for rich Allure reports, and (B) direct `pytest` commands for quick iteration.

### Prerequisites (local)
- **Python 3.11+** (use a virtualenv)
- **Install deps**: `pip install -r requirements.txt`
- **Allure CLI** (optional for HTML reports): `brew install allure` on macOS. If missing, raw `allure-results` are still created.
- **Environment configuration**: Create a `.env` file at the repo root with:
  ```
  API_KEY=<your-key>
  API_SECRET=<your-secret>
  ACCOUNT_ID=<your-account-id>
  BASE_URL=https://api-dev.aquanow.io
  DELIVER_QUANTITY=100
  ```


### A) Using the project helper (recommended for Allure + history)
Purpose: Runs pytest with `--alluredir`, copies previous report history, generates Allure HTML, and opens it.

**Common workflows**:
- Run entire smoke suite:
  ```bash
  python run_suites.py
  ```
  (Adjust `run_suites.py` to call the desired `run_tests(...)` invocation.)

- Call `run_tests()` directly from Python:
  ```bash
  python -c "from test_runner import run_tests; run_tests('smoke', open_report=True)"
  ```

**Notes**:
- `run_tests()` creates timestamped folders under `allure-results/<suite>/<timestamp>` and `reports/<suite>/<timestamp>`.
- Runs `pytest` with `--alluredir` and `--html` flags.
- Attempts `allure generate` and `allure open` (requires Allure CLI).
- If Allure CLI is unavailable, raw `allure-results` are still generated for later processing.

### B) Running tests directly in terminal (fast iteration / debugging)
Purpose: Use `pytest` directly for TDD cycles, debugging failures, and running small subsets quickly.

**Useful flags and examples**:

- Run all tests:
  ```bash
  pytest -vv
  ```

- Run a single test file:
  ```bash
  pytest src/test/aquanow/tests/test_rfq_quote.py -vv -s
  ```

- Run tests by marker:
  ```bash
  pytest -m smoke            # All smoke tests
  pytest -m regression       # All regression tests
  pytest -m negative         # All negative tests
  pytest -m rfq              # All RFQ tests
  ```

- Run tests matching a pattern (by test name):
  ```bash
  pytest -k "create_quote" -vv
  ```

- Run a single test class:
  ```bash
  pytest src/test/aquanow/tests/test_rfq_quote.py::TestRFQQuote -vv
  ```

- Run a single parametrized test case:
  ```bash
  pytest src/test/aquanow/tests/test_rfq_quote.py::TestRFQQuote::test_create_rfq_quote_positive_matrix[buy_deliver_quantity] -vv -s
  ```

- Stop on first failure (fast feedback):
  ```bash
  pytest -x -q
  ```

- Run and generate Allure results:
  ```bash
  pytest --alluredir=allure-results/smoke -vv
  ```

- Run with print output visible:
  ```bash
  pytest -s -vv
  ```

### Tips and troubleshooting
- **Missing `.env`**: Tests will skip or fail. Ensure `.env` exists or CI variables are set.
- **Allure CLI not found**: Install with `brew install allure` on macOS. Tests will still run; Allure report generation will fail.
- **Fixture errors**: Check `conftest.py` if a fixture is not found. Common issue: fixture scope mismatch (e.g., function-scoped fixture used in session-scoped test).
- **Slow first run**: Model downloads or API calls might be slow. Subsequent runs are faster.
- **Debug a single test easily**: Run with `-s -k <test_name>` and add `print()` statements or use `pytest --pdb` to drop into the debugger on failure.

### Generating and opening Allure report manually
```bash
# Generate HTML (requires Allure CLI)
allure generate allure-results/smoke/<timestamp> -o reports/smoke/<timestamp> --clean

# Open in browser (macOS)
open reports/smoke/<timestamp>/index.html
```


## Allure reporting
- **Reporting setup**: Tests use `--alluredir` (runners already do this) to produce raw `allure-results`.
- **Trend charts**: `test_runner.py` automates copying the `history` folder so Allure trend graphs show test history over time.
- **HTML generation**: Run `allure generate` to produce the HTML dashboard.
- **Attaching artifacts**: Use `allure.attach()` to attach payloads, responses, and logs. Example:
  ```python
  import allure
  allure.attach(json.dumps(response.json()), name='response', attachment_type=allure.attachment_type.JSON)
  ```
- **Dynamic test titles/parameters**: Use `allure.dynamic.title()` and `allure.dynamic.parameter()` to enrich test reports at runtime.
- **Steps and severity**: Use `allure.step()` context managers to break tests into logical steps. Use `@allure.severity()` to mark test importance.

## CI recommendations
CI pipeline should:
1. **Install dependencies** (cache pip wheels for speed):
   ```bash
   pip install -r requirements.txt
   ```
2. **Set environment variables securely** (avoid hardcoding secrets):
   - `API_KEY`, `API_SECRET`, `ACCOUNT_ID`, `BASE_URL` via CI secrets/masked variables.
3. **Run tests** and collect artifacts:
   ```bash
   python -c "from test_runner import run_tests; run_tests('smoke')"
   ```
4. **Archive Allure results and HTML reports**:
   - Save `allure-results/<suite>/` and `reports/<suite>/` for later processing or inspection.
5. **Publish reports** (optional):
   - Upload HTML to artifact storage or push to Allure Server.
   - Generate trend history for visibility.

**Example CI snippet** (pseudo-YAML):
```yaml
# Install
pip install -r requirements.txt

# Set secrets as environment variables
export API_KEY=${{ secrets.API_KEY }}
export API_SECRET=${{ secrets.API_SECRET }}
export ACCOUNT_ID=${{ secrets.ACCOUNT_ID }}

# Run tests
python -c "from test_runner import run_tests; run_tests('smoke')"

# Collect artifacts
artifacts:
  - allure-results/smoke/
  - reports/smoke/
```

## Writing good tests (rules of thumb)
- **Single responsibility**: One major assertion per test. Group closely-related assertions (e.g., response contract validation) but avoid testing multiple independent features in one test.
- **Arrange/Act/Assert structure**: Organize test code clearly:
  1. **Arrange**: Set up test data and preconditions.
  2. **Act**: Execute the API call or action being tested.
  3. **Assert**: Validate the response and side effects.
- **Avoid sleeps**: Use explicit polling or test utilities (retry with timeout) if async behavior is needed. Sleeps make tests slow and flaky.
- **Keep tests deterministic**: Mock or stub external flaky endpoints when possible. Avoid time-dependent assertions.
- **Keep tests small and fast**: Each test should complete in under 5 seconds (excluding network latency). Expensive integration tests belong in separate CI jobs.
- **Use allure steps**: Break complex tests into logical steps for better reporting and debugging.
- **Parameterize, don't duplicate**: Use `@pytest.mark.parametrize` with test case matrices (from `rfq_test_data.py`) instead of writing near-duplicate test functions.

## Markers, parametrize, and selective runs
- Use `@pytest.mark.<marker>` (e.g., `@pytest.mark.regressionSearch`) to group tests.
- Parameterize cases with `@pytest.mark.parametrize` for table-driven tests instead of multiple near-duplicate tests.

## Debugging and logs
- Run tests with `-s -vv` to view print output.
- Use `allure.attach` to attach HTTP request/response bodies to make failures easier to triage.

## How to add a new test (checklist)
1. Add a file under the appropriate folder in `src/test/aquanow/tests/<suite>/` named `test_<feature>.py`.
2. Use an existing fixture from `conftest.py` or add a new fixture there if it should be shared.
3. Add a marker if needed (e.g., `@pytest.mark.smoke`).
4. Run the test locally with `pytest <path>` and confirm Allure artifacts are created.
5. Open Allure report (`allure serve allure-results/<suite>/<timestamp>`) or use `run_suites.py` to generate HTML.





