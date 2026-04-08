# QA Automation Playground

A comprehensive, portfolio-ready QA automation project demonstrating API testing, UI end-to-end testing, load/performance testing, and BDD -- built with both Python and TypeScript toolchains against real-world practice applications.

---

![API Tests](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/qa-automation-playground/api-tests.yml?label=API%20Tests&style=flat-square)
![UI Tests](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/qa-automation-playground/ui-tests.yml?label=UI%20Tests&style=flat-square)
![Load Tests](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/qa-automation-playground/load-tests.yml?label=Load%20Tests&style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

---

## Architecture

```
+---------------------+       +---------------------------+
|   Test Suites       |       |   Target Applications     |
|                     |       |                           |
|  API Tests  --------+------>|  DummyJSON API            |
|  (pytest + httpx)   |       |  https://dummyjson.com    |
|                     |       |                           |
|  UI Tests  ---------+------>|  Sauce Demo               |
|  (Playwright)       |       |  https://saucedemo.com    |
|                     |       |                           |
|  Load Tests  -------+------>|  DummyJSON API            |
|  (Locust / k6)      |       |  https://dummyjson.com    |
|                     |       |                           |
|  BDD Tests  --------+------>|  Sauce Demo               |
|  (behave/Gherkin)   |       |  https://saucedemo.com    |
+---------------------+       +---------------------------+
         |
         v
+---------------------+
|   Reporting         |
|  Allure  |  k6 HTML |
+---------------------+
```

---

## Tech Stack

| Area            | Python                          | TypeScript                |
| --------------- | ------------------------------- | ------------------------- |
| Test Runner     | pytest                          | vitest                    |
| HTTP Client     | httpx                           | fetch / Playwright API    |
| Validation      | pydantic                        | zod                       |
| UI Automation   | playwright (Python)             | playwright (TS)           |
| Load Testing    | locust                          | k6                        |
| BDD             | behave                          | --                        |
| Reporting       | allure-pytest                   | allure / k6 HTML          |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Git

### Clone

```bash
git clone https://github.com/YOUR_USERNAME/qa-automation-playground.git
cd qa-automation-playground
```

### Python Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

pip install -r requirements.txt
playwright install chromium
```

### TypeScript Setup

```bash
npm install
npx playwright install chromium
```

### Run Tests

```bash
# --- Python ---
pytest tests/api/ -v                          # API tests
pytest tests/ui/ -v                           # UI E2E tests
locust -f tests/load/locustfile.py --headless # Load tests (headless)
pytest tests/bdd/ -v                          # BDD tests

# --- TypeScript ---
npx vitest run tests/api                      # API tests
npx playwright test tests/ui                  # UI E2E tests
k6 run tests/load/smoke.js                    # Load tests
```

### Generate Reports

```bash
# Allure (Python)
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results

# k6 HTML
k6 run --out json=reports/k6-results.json tests/load/smoke.js
```

---

## Test Coverage Summary

| Layer      | Count          | Description                                          |
| ---------- | -------------- | ---------------------------------------------------- |
| API Tests  | 25 test cases  | Auth, products CRUD, carts, users, search, pagination |
| UI Tests   | 15 E2E flows   | Login, inventory, cart, checkout, sorting, logout      |
| Load Tests | 3 scenarios    | Smoke (10 VUs), Average (50 VUs), Stress (200 VUs)    |
| BDD        | 5 scenarios    | Login, add-to-cart, checkout (Gherkin feature files)   |

---

## Reports

- **Allure** -- rich HTML reports with step-level detail, screenshots on failure, and historical trend charts. Generated from pytest runs.
- **k6 HTML / JSON** -- throughput, latency percentiles (p50/p95/p99), error rates, and VU concurrency graphs for load test scenarios.

---

## Project Structure

```
qa-automation-playground/
|-- python/
|   |-- tests/
|   |   |-- api/              # API test modules (pytest + httpx)
|   |   |-- ui/               # UI E2E tests (Playwright Python)
|   |   |-- load/             # Load tests (Locust)
|   |   |-- bdd/
|   |   |   |-- features/     # Gherkin .feature files
|   |   |   |-- steps/        # Step definitions
|   |   |-- conftest.py       # Shared fixtures
|   |-- src/
|   |   |-- models/           # Pydantic response models
|   |   |-- clients/          # HTTP client wrappers
|   |   |-- pages/            # Page Object Model classes
|   |   |-- utils/            # Helpers, data generators
|   |-- requirements.txt
|   |-- pytest.ini
|
|-- typescript/
|   |-- tests/
|   |   |-- api/              # API tests (vitest + zod)
|   |   |-- ui/               # UI E2E tests (Playwright TS)
|   |   |-- load/             # k6 load test scripts
|   |-- src/
|   |   |-- schemas/          # Zod validation schemas
|   |   |-- clients/          # HTTP client wrappers
|   |   |-- pages/            # Page Object Model classes
|   |-- package.json
|   |-- tsconfig.json
|   |-- playwright.config.ts
|   |-- vitest.config.ts
|
|-- target-apps/
|   |-- APPS.md               # Documentation of all target applications
|
|-- reports/                  # Generated reports (gitignored)
|-- .github/
|   |-- workflows/
|       |-- api-tests.yml
|       |-- ui-tests.yml
|       |-- load-tests.yml
|
|-- README.md
|-- TEST_STRATEGY.md
|-- CONTRIBUTING.md
|-- LICENSE
```

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
