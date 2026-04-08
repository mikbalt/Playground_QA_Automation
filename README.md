# QA Automation Playground

A comprehensive, portfolio-ready QA automation project demonstrating **API testing, UI E2E testing, Load/Performance testing, and BDD** — built with both **Python & TypeScript** against real-world practice applications.

> Lihat [LEARNING_GUIDE.md](LEARNING_GUIDE.md) untuk panduan belajar step-by-step.

---

![API Tests](https://img.shields.io/github/actions/workflow/status/mikbalt/Playground_QA_Automation/test-pipeline.yml?label=CI%20Pipeline&style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

---

## Architecture

```
┌─────────────────────┐       ┌──────────────────────────┐
│   Test Suites        │       │   Target Applications     │
│                      │       │                           │
│  API Tests (Python)  ├──────►│  DummyJSON REST API       │
│  pytest + httpx      │       │  https://dummyjson.com    │
│                      │       │                           │
│  API Tests (TS)      ├──────►│  Countries GraphQL API    │
│  Vitest + Zod        │       │  countries.trevorblades.. │
│                      │       │                           │
│  UI Tests (Py + TS)  ├──────►│  Sauce Demo               │
│  Playwright POM      │       │  https://saucedemo.com    │
│                      │       │                           │
│  BDD (Gherkin)       ├──────►│  Sauce Demo               │
│  pytest-bdd          │       │                           │
│                      │       │                           │
│  Load Tests          ├──────►│  DummyJSON REST API       │
│  k6 + Locust         │       │                           │
└──────────┬───────────┘       └───────────────────────────┘
           │
           ▼
┌──────────────────────┐
│   Reporting           │
│  Allure  │  k6 HTML   │
└──────────────────────┘
```

---

## Tech Stack

| Area | Python | TypeScript/JS |
|---|---|---|
| Test Runner | pytest | Vitest / Playwright Test |
| HTTP Client | httpx | native fetch |
| Schema Validation | Pydantic v2 | Zod |
| UI Automation | Playwright (sync) | Playwright |
| Load Testing | Locust | k6 |
| BDD | pytest-bdd + Gherkin | — |
| Reporting | allure-pytest | k6 HTML / Playwright HTML |

---

## Quick Start

### Prerequisites

- **Python 3.12+** (64-bit) — [python.org](https://python.org)
- **Node.js 20+** — [nodejs.org](https://nodejs.org)
- **Git** — [git-scm.com](https://git-scm.com)

### 1. Clone & Setup

```bash
git clone https://github.com/mikbalt/Playground_QA_Automation.git
cd Playground_QA_Automation

# Python dependencies
pip install -r api-tests/requirements.txt
playwright install chromium

# TypeScript dependencies
cd api-tests/typescript && npm install && cd ../..
cd ui-tests/typescript && npm install && npx playwright install chromium && cd ../..
```

### 2. Run Tests

```bash
# ── API Tests (Python) ──
python -m pytest api-tests/tests/ -v -p no:playwright

# ── API Tests (TypeScript) ──
cd api-tests/typescript && npx vitest run

# ── UI Tests (Python Playwright) ──
python -m pytest ui-tests/python/tests/ -v

# ── UI Tests (TypeScript Playwright) ──
cd ui-tests/typescript && npx playwright test --project=chromium

# ── BDD Tests ──
python -m pytest bdd/ -v

# ── Load Tests (k6) ──
k6 run load-tests/k6/scenarios/smoke.js

# ── Load Tests (Locust) ──
python -m locust -f load-tests/locust/locustfile.py --host=https://dummyjson.com
```

### 3. Generate Reports

```bash
# Allure Report
python -m pytest api-tests/tests/ --alluredir=reports/allure-results -v
allure serve reports/allure-results

# Playwright HTML Report
cd ui-tests/typescript && npx playwright show-report
```

---

## Test Coverage

| Layer | Count | Framework | Target App |
|---|---|---|---|
| API (Python) | 35 tests | pytest + httpx + pydantic | DummyJSON + Countries API |
| API (TypeScript) | 15 tests | Vitest + Zod | DummyJSON |
| UI (Python) | 15 tests | Playwright + POM | Sauce Demo |
| UI (TypeScript) | 8 tests | Playwright | Sauce Demo |
| BDD | 9 scenarios | pytest-bdd + Gherkin | Sauce Demo |
| Load | 4 scenarios | k6 | DummyJSON |
| Load | 1 config | Locust | DummyJSON |
| **Total** | **87 tests** | | |

---

## Project Structure

```
qa-automation-playground/
├── README.md                          ← Kamu di sini
├── LEARNING_GUIDE.md                  ← Panduan belajar day-by-day
├── TEST_STRATEGY.md                   ← Dokumen strategi (level senior)
├── CONTRIBUTING.md                    ← Naming conventions & rules
│
├── target-apps/
│   └── APPS.md                        ← Dokumentasi target apps
│
├── api-tests/                         ← Python: pytest + httpx
│   ├── conftest.py                    ← Fixtures (base_url, auth_token, client)
│   ├── requirements.txt               ← Python dependencies
│   ├── models/                        ← Pydantic v2 schema models
│   ├── clients/                       ← HTTP client abstraction
│   ├── tests/
│   │   ├── test_auth.py               ← 7 auth tests
│   │   ├── test_products.py           ← 14+ product tests
│   │   ├── test_cart.py               ← 6 cart tests
│   │   └── test_graphql.py            ← 6 GraphQL tests
│   ├── typescript/                    ← Vitest + Zod
│   │   ├── auth.test.ts
│   │   ├── products.test.ts
│   │   └── cart.test.ts
│   └── postman/
│       └── dummyjson.collection.json  ← Postman collection (11 requests)
│
├── ui-tests/
│   ├── python/                        ← Playwright Python + POM
│   │   ├── pages/                     ← Page Object classes
│   │   ├── components/                ← Reusable UI components
│   │   ├── tests/                     ← 15 E2E test cases
│   │   └── data/                      ← Test data (users, credentials)
│   └── typescript/                    ← Playwright TypeScript
│       ├── pages/                     ← Page Object classes
│       └── tests/                     ← 8 E2E test specs
│
├── bdd/                               ← Gherkin + pytest-bdd
│   ├── features/                      ← .feature files (login, checkout, product)
│   ├── steps/                         ← Step definitions (test_*.py)
│   └── conftest.py                    ← Browser fixtures + shared steps
│
├── load-tests/
│   ├── k6/scenarios/                  ← smoke, load, stress, checkout_load
│   │   └── thresholds.js             ← Shared threshold configs
│   └── locust/
│       └── locustfile.py              ← Locust load test config
│
├── reports/                           ← Generated (gitignored)
│
└── .github/workflows/
    └── test-pipeline.yml              ← CI/CD: 6 parallel jobs
```

---

## Documentation

| Document | Isi |
|---|---|
| [LEARNING_GUIDE.md](LEARNING_GUIDE.md) | Panduan belajar 3 hari, step-by-step, ada latihan mandiri |
| [TEST_STRATEGY.md](TEST_STRATEGY.md) | Test strategy document (scope, risk, DoD) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Naming conventions, PR guidelines |
| [target-apps/APPS.md](target-apps/APPS.md) | Dokumentasi semua target app + credentials |

---

## License

MIT
