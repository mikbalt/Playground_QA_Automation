# Target Applications

This document describes every third-party application used as a test target in this project, including URLs, credentials, capabilities, and which test layers exercise them.

---

## 1. DummyJSON

| Field           | Value                                     |
| --------------- | ----------------------------------------- |
| **URL**         | https://dummyjson.com                     |
| **Docs**        | https://dummyjson.com/docs                |
| **Type**        | REST API (public, no API key required)    |
| **Used For**    | API functional tests, API contract tests, load/performance tests |

### Description

DummyJSON is a free, fake REST API that provides realistic JSON data for prototyping and testing. It supports authentication (JWT), CRUD operations, search, filtering, pagination, and more -- making it ideal for exercising a wide range of API test scenarios.

### Key Endpoints

| Method | Endpoint                        | Purpose                        |
| ------ | ------------------------------- | ------------------------------ |
| POST   | `/auth/login`                   | Authenticate and receive JWT   |
| GET    | `/auth/me`                      | Get current authenticated user |
| GET    | `/products`                     | List all products (paginated)  |
| GET    | `/products/{id}`                | Get single product by ID       |
| GET    | `/products/search?q={query}`    | Search products by keyword     |
| GET    | `/products/categories`          | List product categories        |
| GET    | `/carts`                        | List all carts                 |
| GET    | `/carts/{id}`                   | Get single cart by ID          |
| GET    | `/users`                        | List all users                 |
| GET    | `/users/{id}`                   | Get single user by ID          |

### Test Credentials

| Field      | Value           |
| ---------- | --------------- |
| Username   | `emilys`        |
| Password   | `emilyspass`    |

> These are built-in demo credentials provided by DummyJSON. See their docs for additional test users.

### Test Layers

- **API Tests** -- Auth flow, CRUD on products/carts/users, search, pagination, error handling, schema validation.
- **Load Tests** -- Smoke, average, and stress scenarios targeting product listing and search endpoints.

---

## 2. REST Countries API

| Field           | Value                                         |
| --------------- | --------------------------------------------- |
| **URL**         | https://restcountries.com                     |
| **Docs**        | https://restcountries.com/#endpoints          |
| **Type**        | REST API (public, no authentication)          |
| **Used For**    | Supplementary API tests, schema validation    |

### Description

REST Countries provides information about countries (name, capital, population, region, languages, currencies, etc.) via a simple REST API. No authentication is required. It is useful for practicing GET-only API tests with rich, nested JSON responses.

### Key Endpoints

| Method | Endpoint                        | Purpose                        |
| ------ | ------------------------------- | ------------------------------ |
| GET    | `/v3.1/all`                     | List all countries             |
| GET    | `/v3.1/name/{name}`             | Search by country name         |
| GET    | `/v3.1/alpha/{code}`            | Get country by code (e.g. US) |
| GET    | `/v3.1/region/{region}`         | Filter by region               |

### Test Credentials

None required -- fully public API.

### Test Layers

- **API Tests** -- Response schema validation, filtering, searching, edge cases (invalid country codes, empty results).

---

## 3. Sauce Demo

| Field           | Value                                     |
| --------------- | ----------------------------------------- |
| **URL**         | https://www.saucedemo.com                 |
| **Type**        | Web application (static, no backend API)  |
| **Used For**    | UI E2E tests, BDD acceptance tests        |

### Description

Sauce Demo is a sample e-commerce web application built by Sauce Labs specifically for practicing UI automation. It features a login page, product inventory, shopping cart, and multi-step checkout flow. Several built-in user accounts simulate different behaviors (standard, locked-out, glitchy, slow).

### Test Credentials

| Username                | Password           | Behavior                                 |
| ----------------------- | ------------------- | ---------------------------------------- |
| `standard_user`         | `secret_sauce`      | Normal, fully functional user            |
| `locked_out_user`       | `secret_sauce`      | Login is blocked -- shows error message  |
| `problem_user`          | `secret_sauce`      | Broken images, glitchy form behavior     |
| `performance_glitch_user` | `secret_sauce`    | Intentionally slow responses             |
| `error_user`            | `secret_sauce`      | Random errors during checkout            |
| `visual_user`           | `secret_sauce`      | Visual inconsistencies for visual testing |

### Key Pages & Flows

| Page / Flow        | URL Path                  | Purpose                              |
| ------------------ | ------------------------- | ------------------------------------ |
| Login              | `/`                       | Authentication entry point           |
| Inventory          | `/inventory.html`         | Product listing with sort options    |
| Product Detail     | `/inventory-item.html`    | Single product view                  |
| Cart               | `/cart.html`              | Shopping cart with item management   |
| Checkout Step 1    | `/checkout-step-one.html` | Shipping information form            |
| Checkout Step 2    | `/checkout-step-two.html` | Order summary and confirmation       |
| Checkout Complete  | `/checkout-complete.html` | Order success page                   |

### Test Layers

- **UI E2E Tests** -- Login (valid, invalid, locked-out), inventory browsing, product sorting, add/remove cart items, full checkout flow, logout.
- **BDD Tests** -- Gherkin scenarios for login, add-to-cart, and checkout flows using `standard_user`.

---

## 4. TodoMVC

| Field           | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| **URL**         | https://todomvc.com/examples/react/dist/                     |
| **Docs**        | https://todomvc.com                                          |
| **Type**        | Web application (client-side only, no backend)               |
| **Used For**    | Supplementary UI tests, Playwright practice                  |

### Description

TodoMVC is a well-known project that implements the same to-do application in many JavaScript frameworks. The React version is used here as a lightweight UI automation target for practicing fundamental Playwright interactions: typing, clicking, keyboard shortcuts, assertions on dynamic lists.

### Key Interactions

| Action               | How                                                |
| -------------------- | -------------------------------------------------- |
| Add a todo           | Type in the input field and press Enter             |
| Complete a todo      | Click the checkbox next to the item                 |
| Delete a todo        | Hover over the item and click the destroy button    |
| Edit a todo          | Double-click the label, modify text, press Enter    |
| Filter (All/Active/Completed) | Click the filter links at the bottom      |
| Clear completed      | Click "Clear completed" button                      |

### Test Credentials

None -- no authentication. The app runs entirely in the browser with no server state.

### Test Layers

- **UI Tests** -- CRUD operations on todos, filtering, bulk actions, keyboard navigation. Used as a simpler warm-up target before tackling Sauce Demo flows.

---

## General Notes

- **Rate Limits:** DummyJSON and REST Countries are public APIs. Be respectful with load tests. Keep virtual user counts reasonable and add ramp-up periods.
- **Availability:** All target apps are third-party hosted. If an app is down, tests will fail through no fault of your code. Consider adding retry logic or skip markers for CI resilience.
- **Data Mutability:** DummyJSON simulates mutations (POST, PUT, DELETE) but does not persist changes. Each request returns a plausible response, but the underlying data resets. Design tests accordingly -- never assert on data created by a previous test run.
- **Browser Requirements:** Sauce Demo and TodoMVC require a modern browser. Playwright's bundled Chromium is sufficient for all UI tests.
