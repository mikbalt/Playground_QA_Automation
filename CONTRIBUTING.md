# Contributing

Thank you for your interest in contributing to the QA Automation Playground. This document covers naming conventions, folder structure rules, pull request guidelines, and test naming patterns to keep the project consistent and maintainable.

---

## Table of Contents

1. [Folder Structure Rules](#folder-structure-rules)
2. [Naming Conventions](#naming-conventions)
3. [Test Naming Patterns](#test-naming-patterns)
4. [Code Style & Linting](#code-style--linting)
5. [Pull Request Guidelines](#pull-request-guidelines)
6. [Commit Message Format](#commit-message-format)

---

## Folder Structure Rules

```
python/
  tests/
    api/           # One file per API resource (e.g., test_products.py, test_auth.py)
    ui/            # One file per page or flow (e.g., test_login.py, test_checkout.py)
    load/          # One locustfile per scenario group
    bdd/
      features/    # One .feature file per user story
      steps/       # Step definitions, grouped by domain
  src/
    models/        # Pydantic models -- one file per API resource
    clients/       # HTTP client wrappers -- one file per service
    pages/         # Page Object classes -- one file per page
    utils/         # Stateless helpers (data generators, formatters)

typescript/
  tests/
    api/           # One file per API resource (e.g., products.test.ts)
    ui/            # One file per page or flow (e.g., login.spec.ts)
    load/          # k6 scripts -- one file per scenario
  src/
    schemas/       # Zod schemas -- one file per API resource
    clients/       # HTTP client wrappers
    pages/         # Page Object classes
```

### Rules

1. **No test logic in `src/`.** The `src/` directory contains only helpers, models, clients, and page objects. Assertions live in `tests/`.
2. **One concern per file.** A test file covers a single resource, page, or flow. If a file exceeds ~300 lines, split it.
3. **Shared fixtures go in `conftest.py`** (Python) or a `fixtures/` directory (TypeScript).
4. **Generated files go in `reports/`** and must be gitignored.

---

## Naming Conventions

### Files

| Language   | Layer   | Pattern                          | Example                    |
| ---------- | ------- | -------------------------------- | -------------------------- |
| Python     | API     | `test_<resource>.py`             | `test_products.py`         |
| Python     | UI      | `test_<page_or_flow>.py`         | `test_checkout.py`         |
| Python     | Load    | `locustfile_<scenario>.py`       | `locustfile_smoke.py`      |
| Python     | BDD     | `<story>.feature`                | `login.feature`            |
| Python     | Model   | `<resource>_model.py`            | `product_model.py`         |
| Python     | Page    | `<page>_page.py`                 | `login_page.py`            |
| TypeScript | API     | `<resource>.test.ts`             | `products.test.ts`         |
| TypeScript | UI      | `<page_or_flow>.spec.ts`         | `checkout.spec.ts`         |
| TypeScript | Load    | `<scenario>.k6.ts`               | `smoke.k6.ts`              |
| TypeScript | Schema  | `<resource>.schema.ts`           | `product.schema.ts`        |
| TypeScript | Page    | `<page>.page.ts`                 | `login.page.ts`            |

### Classes & Functions

| Element              | Convention          | Example                          |
| -------------------- | ------------------- | -------------------------------- |
| Python class         | PascalCase          | `LoginPage`, `ProductModel`      |
| Python function      | snake_case          | `test_login_valid_user`          |
| Python fixture       | snake_case          | `authenticated_client`           |
| TypeScript class     | PascalCase          | `LoginPage`, `ProductSchema`     |
| TypeScript function  | camelCase           | `testLoginValidUser`             |
| TypeScript test name | Descriptive string  | `"should return 200 for valid product ID"` |
| Gherkin scenario     | Sentence case       | `"User logs in with valid credentials"`    |

### Variables & Constants

- Python: `snake_case` for variables, `UPPER_SNAKE_CASE` for constants.
- TypeScript: `camelCase` for variables, `UPPER_SNAKE_CASE` for constants.

---

## Test Naming Patterns

Good test names describe the **action** and the **expected outcome**. Follow these patterns.

### Python (pytest)

```python
# Pattern: test_<action>_<expected_outcome>

def test_login_with_valid_credentials_returns_token():
    ...

def test_login_with_invalid_password_returns_401():
    ...

def test_get_product_by_id_returns_correct_schema():
    ...

def test_add_to_cart_increases_item_count():
    ...
```

### TypeScript (vitest)

```typescript
// Pattern: describe("<Resource>") > it("should <outcome> when <condition>")

describe("Products API", () => {
  it("should return 200 and a valid product for a known ID", async () => {
    ...
  });

  it("should return 404 when product ID does not exist", async () => {
    ...
  });
});
```

### TypeScript (Playwright)

```typescript
// Pattern: test("<user action> -- <expected result>")

test("login with valid credentials -- redirects to inventory", async ({ page }) => {
  ...
});

test("checkout with empty cart -- shows error message", async ({ page }) => {
  ...
});
```

### BDD (Gherkin)

```gherkin
Feature: User Login

  Scenario: Successful login with standard user
    Given the user is on the login page
    When the user enters valid credentials
    Then the user is redirected to the inventory page

  Scenario: Failed login with locked-out user
    Given the user is on the login page
    When the user enters locked-out credentials
    Then an error message is displayed
```

---

## Code Style & Linting

### Python

- Formatter: `ruff format`
- Linter: `ruff check`
- Type checking: `mypy --strict`
- Run before committing:

```bash
ruff format python/
ruff check python/ --fix
mypy python/src/
```

### TypeScript

- Formatter: `prettier --write`
- Linter: `eslint`
- Type checking: `tsc --noEmit`
- Run before committing:

```bash
npx prettier --write typescript/
npx eslint typescript/ --fix
npx tsc --noEmit
```

---

## Pull Request Guidelines

### Before Opening a PR

1. **All tests pass locally.** Run the full suite for the layer you changed.
2. **Linting and formatting are clean.** No warnings, no errors.
3. **No unrelated changes.** Keep the diff focused on one concern.
4. **New tests have docstrings or comments** explaining what they validate and why.

### PR Title Format

```
<type>(<scope>): <short description>
```

| Type       | Use When                                    |
| ---------- | ------------------------------------------- |
| `feat`     | Adding new tests or test infrastructure     |
| `fix`      | Fixing a broken or flaky test               |
| `refactor` | Restructuring without changing behavior     |
| `docs`     | Documentation-only changes                  |
| `chore`    | Dependency updates, CI config, tooling      |

Examples:

```
feat(api): add negative tests for product search endpoint
fix(ui): stabilize checkout test with explicit wait for confirmation
refactor(pages): extract shared navigation methods into BasePage
docs: update TEST_STRATEGY with load test thresholds
chore(ci): add Allure report upload to UI test workflow
```

### PR Description Template

```markdown
## What

Brief description of what this PR does.

## Why

Context or motivation for the change.

## Test Evidence

- [ ] All existing tests pass
- [ ] New tests added (count: X)
- [ ] Screenshots / report links (if applicable)

## Checklist

- [ ] Follows naming conventions from CONTRIBUTING.md
- [ ] No hard-coded waits or sleeps
- [ ] Page Objects used for UI tests (no raw selectors in test files)
- [ ] Parameterized where applicable
```

### Review Expectations

- Every PR requires at least one approval.
- Reviewers should check: naming, assertion quality, independence, and readability.
- Address all review comments before merging. Use "Resolve conversation" only after the fix is pushed.

---

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Examples:

```
feat(api): add auth token refresh test

Test covers the scenario where an expired token is used
and the API returns 401, prompting a refresh.

fix(ui): resolve flaky cart removal test

Root cause: race condition between remove click and DOM update.
Fix: wait for cart badge count to update before asserting.
```

Keep the subject line under 72 characters. Use the body for context when the change is not self-explanatory.
