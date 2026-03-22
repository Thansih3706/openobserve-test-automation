# Aquanow RFQ API Automation Exercise

## Overview

This project provides automated API test coverage for Aquanow RFQ trade endpoints, validating core workflows such as quote creation, execution, expiry, and error handling.

The framework is designed for easy setup, fast execution, and minimal configuration, while maintaining strong test structure and scalability.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git
- Virtual environment support

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/thansihkp-tech/aquanow_exercise.git
cd aquanow_exercise
```

### 2. Setup Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Update  `.env` file in the project root directory with your API credentials:

```
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
BASE_URL=https://api-dev.aquanow.io
ACCOUNT_ID=your_account_id_here
```

## How to Execute

### Run Full Test Suite

```bash
python run_suites.py
```

### Run Specific Tests

To run only specific tests, update the `run_suites.py` file to specify which test modules or test cases you want to execute. The file contains configuration options to select test suites.

### Run with Allure Reporting

Generate detailed HTML reports using Allure:

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

The Allure report will open in your default browser showing detailed test results, history, and analytics.

## Test Coverage

### RFQ Operations

#### RFQ Quote
- Get quote (positive & negative scenarios)
- Create quote (positive, negative, validation cases)
- Quantity precedence validation (based on observed behavior)

#### RFQ Execute
- Successful execution
- Expired quote behavior
- Invalid quote ID handling
- Duplicate execution prevention
- Unauthorized execution

#### RFQ Expire
- Successful expiry
- Expiring already expired quote
- Execute after expiry validation

### Authentication Tests
- Missing authentication
- Invalid API key / signature
- Missing headers (API key, signature, nonce)
- Replay / stale nonce scenarios (best-effort based on API behavior)

## Reporting

Allure is used for comprehensive test reporting. After running tests with the `--alluredir` flag, reports are generated in the `reports/allure-results` directory.

**View the report:**

```bash
allure serve reports/allure-results
```

HTML reports are also generated in `reports/html/` for easy sharing and archival.

## Project Structure

```
.
├── src/
│   ├── main/aquanow/
│   │   └── utils/              # API client, authentication, helpers, config
│   └── test/aquanow/
│       └── tests/              # Test cases
├── resources/
│   └── testdata/               # Test data and fixtures
├── reports/                    # Test reports (Allure & HTML)
├── allure-results/             # Allure result data
├── run_suites.py               # Test runner entry point
├── test_runner.py              # Additional test runner utilities
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── pyproject.toml              # Project metadata
└── README.md                   # This file
```

## Troubleshooting

### Common Issues

- **ModuleNotFoundError**: Ensure virtual environment is activated and dependencies are installed with `pip install -r requirements.txt`
- **Authentication Errors**: Verify `.env` file exists in the project root with correct credentials
- **Allure Report Not Generating**: Ensure Allure is installed via `requirements.txt` and the `--alluredir` path exists
- **Connection Timeout**: Check BASE_URL in `.env` file is correct and network connectivity is available