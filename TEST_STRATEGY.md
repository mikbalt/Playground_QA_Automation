# Test Strategy

**Project:** QA Automation Playground
**Author:** QA Engineer
**Last Updated:** 2026-04-08
**Status:** Living Document

---

## 1. Scope

### In Scope

| Area                  | Details                                                         |
| --------------------- | --------------------------------------------------------------- |
| API Functional Tests  | DummyJSON endpoints: auth, products, carts, users, search       |
| API Contract Tests    | Response schema validation with pydantic / zod                  |
| UI End-to-End Tests   | Sauce Demo: login, inventory, cart, checkout, sorting, logout   |
| Load / Performance    | DummyJSON API under synthetic load (smoke, average, stress)     |
| BDD Acceptance Tests  | Sauce Demo critical user journeys in Gherkin                    |

### Out of Scope

- Security / penetration testing (OWASP ZAP, Burp Suite).
- Accessibility testing (axe-core audits).
- Visual regression testing (Percy, Applitools).
- Mobile-native testing (Appium).
- Backend unit testing of the target applications themselves -- they are third-party services we do not own.

---

## 2. Risk-Based Prioritization

Tests are prioritized by business risk. The table below maps critical user paths to their risk level and corresponding test investment.

| Priority | Path / Feature             | Risk if Broken                         | Test Types Applied          |
| -------- | -------------------------- | -------------------------------------- | --------------------------- |
| P0       | Authentication flow        | Complete access loss; all flows blocked | API + UI + Load             |
| P0       | Checkout (end-to-end)      | Revenue loss; order cannot complete     | UI E2E + BDD                |
| P1       | Product listing & search   | Users cannot find products             | API + UI E2E                |
| P1       | Cart add / remove / update | Broken purchase funnel                 | API + UI E2E                |
| P2       | User profile & data        | Degraded experience                    | API                         |
| P2       | Sorting & filtering        | Usability issue, not blocking          | UI E2E                      |
| P3       | Pagination / edge cases    | Minor UX gaps                          | API                         |

> **Rule of thumb:** P0 paths get the widest coverage across multiple test types. P3 paths are covered by a single layer.

---

## 3. Test Environment & Data Strategy

### Environments

| Environment | URL                           | Purpose                     |
| ----------- | ----------------------------- | --------------------------- |
| DummyJSON   | https://dummyjson.com         | API and load test target    |
| Sauce Demo  | https://www.saucedemo.com     | UI E2E and BDD target       |

Both targets are publicly hosted practice applications. No staging or production environments are involved.

### Test Data Strategy

| Approach             | When Used                                        |
| -------------------- | ------------------------------------------------ |
| Static fixtures      | Known-good payloads for API contract validation   |
| Parameterized data   | pytest parametrize / vitest each for edge cases   |
| API-seeded state     | Create cart via API before UI checkout test        |
| Built-in credentials | Sauce Demo ships with test users (see APPS.md)    |
| Factory helpers      | Utility functions that generate randomized data   |

> **Principle:** Tests must be independent and idempotent. Each test sets up its own preconditions and does not rely on execution order.

---

## 4. Test Types & Layers

### 4.1 API Tests (pytest + httpx / vitest + fetch)

- **Goal:** Validate endpoint correctness, status codes, response schemas, error handling, and edge cases.
- **Count:** ~25 test cases across auth, products, carts, users, search, and pagination.
- **Assertions:** Status code, JSON schema (pydantic / zod), business rules, response time soft-limits.
- **Data:** Parameterized inputs for positive, negative, and boundary scenarios.

### 4.2 UI End-to-End Tests (Playwright)

- **Goal:** Verify critical user journeys through the browser exactly as a real user would.
- **Count:** ~15 E2E flows covering login, inventory browsing, cart management, checkout, and logout.
- **Pattern:** Page Object Model. Each page is a class encapsulating selectors and actions.
- **Stability:** Auto-waiting, retry-able locators, screenshot-on-failure.

### 4.3 Load / Performance Tests (Locust / k6)

- **Goal:** Measure throughput, latency, and error rates under load to identify performance regressions.
- **Scenarios:**

| Scenario | Virtual Users | Duration | Pass Criteria                    |
| -------- | ------------- | -------- | -------------------------------- |
| Smoke    | 10            | 1 min    | p95 < 500ms, error rate < 1%    |
| Average  | 50            | 5 min    | p95 < 800ms, error rate < 2%    |
| Stress   | 200           | 5 min    | p95 < 2000ms, error rate < 5%   |

### 4.4 BDD / Acceptance Tests (behave + Gherkin)

- **Goal:** Express business-critical scenarios in plain language so non-technical stakeholders can review them.
- **Count:** ~5 scenarios (login, add to cart, remove from cart, checkout happy path, checkout with missing info).
- **Mapping:** Each `.feature` file maps 1:1 to a user story.

---

## 5. Definition of Done -- Per Layer

A test is considered **done** when all of the following are satisfied for its layer.

### API Tests

- [ ] Test covers positive, negative, and at least one boundary case.
- [ ] Response schema is validated (pydantic model or zod schema).
- [ ] Test is parameterized where applicable.
- [ ] Test runs in < 5 seconds.
- [ ] Test passes in CI on a clean checkout.

### UI E2E Tests

- [ ] Page Object class exists for every page touched.
- [ ] No hard-coded waits (`time.sleep` / `page.waitForTimeout`).
- [ ] Screenshot captured on failure.
- [ ] Test is independent -- can run in isolation.
- [ ] Test passes in CI with headless Chromium.

### Load Tests

- [ ] Scenario defines explicit pass/fail thresholds.
- [ ] Results are exported to JSON or HTML for review.
- [ ] Ramp-up and ramp-down phases are configured.
- [ ] Test does not exceed rate limits of target application.

### BDD Tests

- [ ] Feature file is written in Given/When/Then format.
- [ ] Steps are reusable across scenarios.
- [ ] Scenario titles are business-readable.
- [ ] Step definitions delegate to Page Objects (no raw selectors in steps).

---

## 6. Tools & Frameworks

| Category        | Python                     | TypeScript              |
| --------------- | -------------------------- | ----------------------- |
| Test Runner     | pytest 8.x                 | vitest 2.x              |
| HTTP Client     | httpx                      | native fetch             |
| Schema Valid.   | pydantic v2                | zod                     |
| UI Automation   | playwright 1.x (Python)    | playwright 1.x (TS)     |
| Load Testing    | locust 2.x                 | k6 (Grafana)            |
| BDD             | behave 1.x                 | --                       |
| Reporting       | allure-pytest              | allure / k6 HTML         |
| CI/CD           | GitHub Actions             | GitHub Actions           |
| Linting         | ruff, mypy                 | eslint, tsc --noEmit     |
| Formatting      | ruff format                | prettier                 |

---

## 7. Reporting Strategy

### Per-Run Reports

| Report Type     | Tool             | Contents                                        |
| --------------- | ---------------- | ----------------------------------------------- |
| API + UI + BDD  | Allure           | Pass/fail, steps, screenshots, duration, trends |
| Load            | k6 JSON / HTML   | RPS, latency percentiles, error rate, VU graph  |
| Load (Python)   | Locust Web UI    | Real-time charts, downloadable CSV              |

### CI Reports

- Allure results are uploaded as GitHub Actions artifacts on every run.
- A summary comment is posted on the pull request with pass/fail counts and a link to the full Allure report.
- k6 threshold violations cause the CI job to exit non-zero, failing the pipeline.

### Trend Tracking

- Allure history is persisted across runs using the `allure-history` branch pattern, enabling trend charts (pass rate over time, duration drift).

---

## 8. CI/CD Integration

### Pipeline Design

```
push / PR
  |
  +-- api-tests.yml
  |     pytest tests/api/ --alluredir=...
  |
  +-- ui-tests.yml
  |     pytest tests/ui/ --alluredir=...
  |     (or: npx playwright test)
  |
  +-- load-tests.yml  (manual trigger / nightly)
        k6 run tests/load/smoke.js --out json=...
```

### Trigger Rules

| Workflow        | Trigger                                | Timeout |
| --------------- | -------------------------------------- | ------- |
| API Tests       | Every push and PR to `main`            | 10 min  |
| UI Tests        | Every push and PR to `main`            | 15 min  |
| Load Tests      | Manual dispatch or nightly schedule    | 20 min  |

### Failure Handling

- On test failure the workflow uploads:
  - Allure results directory (artifact).
  - Playwright traces and screenshots (artifact).
  - k6 JSON results (artifact).
- Flaky test detection: if a test fails then passes on retry, it is tagged `@flaky` and a tracking issue is opened.

### Branch Protection

- `main` requires all three workflows to pass before merge.
- Load tests are optional on PRs but mandatory on nightly runs.
