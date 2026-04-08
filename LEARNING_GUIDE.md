# QA Automation Bootcamp - Learning Guide

> **Panduan belajar step-by-step untuk menguasai QA Automation dari nol.**
> Ditulis dalam Bahasa Indonesia yang santai tapi tetap informatif.

---

## Cara Menggunakan Repo Ini

Selamat datang di QA Automation Playground! Sebelum mulai, pahami dulu mindset-nya:

1. **Ini bukan sekedar kode jadi** -- ini adalah playground untuk belajar. Jangan cuma baca, tapi jalankan setiap test, ubah kodenya, dan lihat apa yang terjadi.

2. **Setiap folder punya tujuan belajar yang berbeda:**
   - `api-tests/` -- Belajar testing fondasi: API testing (REST + GraphQL)
   - `ui-tests/` -- Belajar testing dari sudut pandang user: UI/E2E testing
   - `bdd/` -- Belajar menulis test dengan bahasa bisnis: Behavior-Driven Development
   - `load-tests/` -- Belajar performance testing: seberapa kuat server-nya?
   - `.github/workflows/` -- Belajar CI/CD: otomatisasi pipeline

3. **Ikuti urutan belajar:** DAY 1 (API) -> DAY 2 (UI + BDD) -> DAY 3 (Load + Polish)

4. **Target aplikasi yang kita test:**

   | App | URL | Kegunaan | Credentials |
   |-----|-----|----------|-------------|
   | DummyJSON | https://dummyjson.com | REST API testing | `emilys` / `emilyspass` |
   | Countries API | https://countries.trevorblades.com/graphql | GraphQL testing | Tidak perlu login |
   | Sauce Demo | https://www.saucedemo.com | UI/E2E testing | `standard_user` / `secret_sauce` |

---

## Prerequisites & Setup

### 1. Install Python 3.12+ (64-bit)

Download dari https://www.python.org/downloads/ dan pastikan centang **"Add Python to PATH"** saat install.

Verifikasi instalasi:
```bash
python --version
# Harus muncul: Python 3.12.x atau lebih tinggi
```

Kalau `python` tidak dikenali, gunakan path lengkap:
```bash
"C:/Users/Admin/AppData/Local/Programs/Python/Python314/python.exe" --version
```

### 2. Install Node.js 20+

Download dari https://nodejs.org/ (pilih LTS). Verifikasi:
```bash
node --version    # Harus v20.x atau lebih tinggi
npm --version     # Ikut terinstall bareng Node.js
```

### 3. Buat Virtual Environment Python

Virtual environment itu ibarat "ruangan khusus" buat project ini, supaya package-nya nggak tercampur sama project lain.

```bash
# Masuk ke folder project
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground

# Buat virtual environment
python -m venv venv

# Aktivasi (di Git Bash / terminal)
source venv/Scripts/activate

# Kalau pakai CMD:
# venv\Scripts\activate

# Kalau berhasil, prompt akan berubah jadi: (venv) $
```

### 4. Install Package Python

```bash
pip install httpx pydantic pytest allure-pytest pytest-bdd playwright locust
```

Penjelasan setiap package:

| Package | Fungsi | Kenapa Kita Pakai? |
|---------|--------|--------------------|
| `httpx` | HTTP client modern | Lebih cepat dari `requests`, support async, API mirip `requests` tapi lebih powerful |
| `pydantic` | Data validation & schema | Validasi response API secara otomatis, kalau field kurang atau tipe salah langsung error |
| `pytest` | Test framework | Framework testing paling populer di Python. Bersih, modular, banyak plugin |
| `allure-pytest` | Reporting | Generate report cantik yang bisa di-share ke team/stakeholder |
| `pytest-bdd` | BDD framework | Menghubungkan Gherkin feature files dengan Python test code |
| `playwright` | Browser automation | Otomatisasi browser modern. Lebih stabil dari Selenium, auto-wait built-in |
| `locust` | Load testing | Load testing berbasis Python dengan web UI yang keren |

### 5. Install Playwright Browsers

```bash
python -m playwright install chromium
```

Ini download browser Chromium yang akan dipakai buat UI testing. Ukurannya sekitar 150MB.

### 6. Install Package Node.js

```bash
# Untuk API tests TypeScript
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/api-tests/typescript
npm install

# Untuk UI tests TypeScript
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/ui-tests/typescript
npm install
npx playwright install chromium
```

Penjelasan package TypeScript:

| Package | Fungsi |
|---------|--------|
| `vitest` | Test framework TypeScript (mirip pytest tapi buat JS/TS) |
| `zod` | Schema validation (mirip Pydantic tapi buat TypeScript) |
| `@playwright/test` | Playwright untuk TypeScript, built-in test runner |

---

## DAY 1: API Testing (Fondasi)

### 1.1 Pahami Dulu: Apa itu API Testing?

**API (Application Programming Interface)** itu ibarat "pintu belakang" sebuah aplikasi. Kalau UI testing itu kita buka browser dan klik-klik, API testing itu kita langsung ngomong ke server-nya.

**Analogi gampang:**
- **UI Testing** = Kamu datang ke restoran, duduk, panggil pelayan, pesan makanan, tunggu, makan
- **API Testing** = Kamu langsung telpon ke dapur dan bilang "Buat nasi goreng 1, kirim ke alamat ini"

**Kenapa API testing itu fondasi?**

Ini namanya Testing Pyramid:

```
        /\
       /  \         <-- UI/E2E Tests (sedikit, lambat, mahal)
      /----\
     /      \       <-- Integration/API Tests (sedang)
    /--------\
   /          \     <-- Unit Tests (banyak, cepat, murah)
  /____________\
```

API tests ada di tengah -- cukup cepat, cukup reliable, dan bisa cover banyak skenario tanpa perlu buka browser.

**REST vs GraphQL:**

| Aspek | REST | GraphQL |
|-------|------|---------|
| Endpoint | Banyak (`/products`, `/users`, `/carts`) | Satu (`/graphql`) |
| Response | Fixed (server yang tentukan) | Flexible (client yang pilih field) |
| HTTP Status | 200, 404, 500, dll | Hampir selalu 200 |
| Error handling | Via HTTP status code | Via `errors` di response body |

Contoh REST:
```
GET /products/1  -->  { "id": 1, "title": "iPhone", "price": 999 ... semua field }
```

Contoh GraphQL:
```graphql
{
  country(code: "ID") {
    name        # Cuma minta name dan capital
    capital     # Nggak perlu field lain
  }
}
```

---

### 1.2 Jalankan API Tests Python

Pastikan kamu sudah di folder project dan virtual environment aktif.

**Jalankan semua API tests:**
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground
python -m pytest api-tests/tests/ -v -p no:playwright
```

Penjelasan setiap flag:
- `python -m pytest` -- Jalankan pytest lewat Python module (lebih reliable daripada `pytest` langsung)
- `api-tests/tests/` -- Folder yang berisi test files
- `-v` -- Verbose mode, tampilkan nama setiap test yang jalan
- `-p no:playwright` -- Disable plugin Playwright supaya nggak bentrok (kita nggak perlu browser buat API tests)

**Jalankan satu file test saja:**
```bash
python -m pytest api-tests/tests/test_auth.py -v -p no:playwright
```

**Jalankan satu test spesifik:**
```bash
python -m pytest api-tests/tests/test_auth.py::TestAuth::test_login_valid_credentials -v -p no:playwright
```

Format-nya: `file_path::ClassName::method_name`

**Jalankan berdasarkan marker:**
```bash
# Smoke tests -- test paling penting, wajib pass
python -m pytest api-tests/tests/ -m smoke -v -p no:playwright

# Regression tests -- test lengkap untuk cek semua fitur
python -m pytest api-tests/tests/ -m regression -v -p no:playwright

# Negative tests -- test yang sengaja pakai input salah
python -m pytest api-tests/tests/ -m negative -v -p no:playwright
```

Penjelasan marker:
- `@pytest.mark.smoke` -- Test kritis. Kalau ini gagal, ada masalah besar. Dijalankan pertama, di setiap deployment.
- `@pytest.mark.regression` -- Test menyeluruh. Dijalankan di CI/CD untuk pastikan semua fitur masih jalan.
- `@pytest.mark.negative` -- Test dengan input yang salah/kosong/invalid. Memastikan error handling benar.

---

### 1.3 Pelajari Kode API Test

#### File: `api-tests/conftest.py` -- Pusat Konfigurasi

```python
import pytest
import httpx

@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for the DummyJSON API."""
    return "https://dummyjson.com"

@pytest.fixture(scope="session")
def auth_token(base_url: str) -> str:
    """Authenticate with DummyJSON and return a valid token."""
    response = httpx.post(
        f"{base_url}/auth/login",
        json={"username": "emilys", "password": "emilyspass"},
    )
    response.raise_for_status()
    data = response.json()
    return data["accessToken"]

@pytest.fixture()
def client(base_url: str) -> httpx.Client:
    """HTTP client pre-configured with the base URL."""
    with httpx.Client(base_url=base_url, timeout=30.0) as c:
        yield c

@pytest.fixture()
def auth_client(base_url: str, auth_token: str) -> httpx.Client:
    """HTTP client pre-configured with the base URL and auth token."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    with httpx.Client(base_url=base_url, headers=headers, timeout=30.0) as c:
        yield c
```

**Apa yang perlu kamu pahami:**

1. **`@pytest.fixture`** -- Ini "penyedia data" untuk test. Daripada setiap test bikin HTTP client sendiri, kita bikin satu kali di sini dan share ke semua test.

2. **`scope="session"`** -- Fixture ini cuma dijalankan SEKALI untuk seluruh test session. Kenapa? Karena `base_url` nggak berubah, dan kita nggak mau login berkali-kali untuk dapat token.

3. **`scope="function"` (default)** -- Fixture ini dijalankan ULANG untuk setiap test function. Kenapa `client` per-function? Supaya setiap test punya koneksi fresh, nggak saling pengaruh.

4. **`yield`** -- Artinya "berikan value ini ke test, dan setelah test selesai, lanjutkan ke baris setelah yield". Ini pattern "setup + teardown". Setelah yield, httpx client akan di-close secara otomatis lewat context manager (`with`).

5. **`auth_client` vs `client`** -- `client` itu tanpa token (bisa akses public endpoint), `auth_client` itu sudah ada Bearer token di header (bisa akses protected endpoint).

---

#### File: `api-tests/models/product.py` -- Schema Validation dengan Pydantic

```python
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    tags: list[str]
    brand: str | None = None      # brand boleh None (optional)
    sku: str
    weight: float
    dimensions: dict[str, float]
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    reviews: list[Any]
    returnPolicy: str
    minimumOrderQuantity: int
    meta: dict[str, Any]
    images: list[str]
    thumbnail: str

class ProductsResponse(BaseModel):
    products: list[Product]
    total: int
    skip: int
    limit: int
```

**Kenapa pakai Pydantic?**

Tanpa Pydantic, kamu harus validasi manual:
```python
# Cara lama (capek, rawan typo):
assert "id" in data
assert isinstance(data["id"], int)
assert "title" in data
assert isinstance(data["title"], str)
# ... dan seterusnya untuk 20+ field
```

Dengan Pydantic, cukup satu baris:
```python
product = Product(**response.json())   # Kalau ada field yang salah tipe, langsung error!
```

Pydantic otomatis:
- Cek semua field ada atau tidak
- Cek tipe data setiap field
- Kasih error message yang jelas kalau ada yang salah
- Handle optional fields (`brand: str | None = None`)

**Ini penting banget di interview!** Schema validation menunjukkan kamu paham contract testing.

---

#### File: `api-tests/tests/test_products.py` -- Contoh Test Lengkap

Beberapa pattern penting yang perlu kamu pahami:

**1. Allure Decorators (untuk reporting):**
```python
@allure.epic("E-Commerce API")        # Kategori besar
@allure.feature("Products")           # Fitur yang ditest
@allure.story("Pagination")           # Cerita spesifik
@allure.title("Pagination with ...")  # Judul test di report
```

**2. Parametrize (jalankan test dengan berbagai input):**
```python
@pytest.mark.parametrize(
    "limit,skip",
    [
        (5, 0),       # Test 1: ambil 5 product dari awal
        (10, 5),      # Test 2: skip 5, ambil 10
        (1, 99),      # Test 3: skip 99, ambil 1
    ],
    ids=["first-5", "skip-5-take-10", "skip-99-take-1"],  # Nama readable di report
)
def test_pagination(self, client, limit, skip):
    response = client.get(f"/products?limit={limit}&skip={skip}")
    assert response.status_code == 200
    data = ProductsResponse(**response.json())
    assert data.limit == limit
    assert data.skip == skip
```

Daripada bikin 3 test function yang mirip-mirip, `parametrize` bikin 1 function yang jalan 3 kali dengan input berbeda. Efisien dan DRY (Don't Repeat Yourself).

**3. CRUD Tests:**
```python
def test_add_product(self, client):       # Create
    response = client.post("/products/add", json=payload)
    assert response.status_code in (200, 201)
    assert data["title"] == payload["title"]
    assert "id" in data                    # Server generate ID baru

def test_update_product(self, client):     # Update
    response = client.put("/products/1", json={"title": "Updated"})
    assert data["title"] == "Updated Product Title"

def test_delete_product(self, client):     # Delete
    response = client.delete("/products/1")
    assert data["isDeleted"] is True       # Soft delete
```

**4. Negative Testing:**
```python
def test_get_nonexistent_product_returns_404(self, client):
    response = client.get("/products/99999")  # Product yang nggak ada
    assert response.status_code == 404
```

Negative test itu penting banget! Kamu nggak cuma test "happy path" (yang benar), tapi juga test "apa yang terjadi kalau salah?"

---

#### File: `api-tests/tests/test_auth.py` -- Authentication Testing

```python
class TestAuth:
    LOGIN_URL = "/auth/login"
    VALID_USERNAME = "emilys"
    VALID_PASSWORD = "emilyspass"

    def test_login_valid_credentials(self, client):
        response = client.post(self.LOGIN_URL,
            json={"username": self.VALID_USERNAME, "password": self.VALID_PASSWORD})
        assert response.status_code == 200
        assert "accessToken" in data        # Dapat token!

    def test_login_invalid_credentials(self, client):
        response = client.post(self.LOGIN_URL,
            json={"username": "invaliduser", "password": "wrongpassword"})
        assert response.status_code == 400  # Bad request!

    def test_access_protected_endpoint_with_token(self, auth_client):
        response = auth_client.get("/auth/me")  # Pakai auth_client (ada token)
        assert response.status_code == 200
        assert "username" in data

    def test_access_protected_endpoint_without_token(self, client):
        response = client.get("/auth/me")        # Pakai client biasa (nggak ada token)
        assert response.status_code == 401       # Unauthorized!
```

**Yang perlu dipahami:**
- Login mengembalikan `accessToken` (JWT token)
- Token dipakai di header: `Authorization: Bearer <token>`
- Endpoint `/auth/me` itu protected -- butuh token
- Tanpa token, server return 401 (Unauthorized)
- Dengan token invalid/expired, server juga return 401

---

#### File: `api-tests/tests/test_graphql.py` -- GraphQL Testing

```python
GRAPHQL_URL = "https://countries.trevorblades.com/graphql"

def test_get_single_country(self):
    query = """
    {
        country(code: "ID") {
            code
            name
            capital
            currency
            continent { name }
        }
    }
    """
    response = httpx.post(GRAPHQL_URL, json={"query": query}, timeout=30.0)
    assert response.status_code == 200
    country = data["data"]["country"]
    assert country["name"] == "Indonesia"
```

**Perbedaan kunci dengan REST:**

```python
# GraphQL: error ada di response BODY, bukan HTTP status
def test_graphql_always_returns_200(self):
    query = '{ totallyBogusQuery { doesNotExist } }'
    response = httpx.post(GRAPHQL_URL, json={"query": query})
    assert response.status_code == 200   # HTTP tetap 200!
    # Error-nya ada di sini:
    assert "errors" in data              # {"errors": [{"message": "..."}]}
```

Ini salah satu hal yang sering ditanya di interview: "Gimana cara handle error di GraphQL?" Jawabannya: kamu nggak bisa cuma cek HTTP status -- kamu harus parsing response body dan cek ada `errors` field atau tidak.

---

#### File: `api-tests/clients/api_client.py` -- Abstraction Pattern

```python
class ApiClient:
    def __init__(self, base_url, token=None, timeout=30.0):
        self.base_url = base_url
        self.token = token

    def get(self, path, params=None):
        client = self._ensure_client()
        return client.get(path, params=params)

    def post(self, path, json=None):
        client = self._ensure_client()
        return client.post(path, json=json)

    def set_token(self, token):
        self.token = token
        self.close()                    # Recreate client dengan token baru
```

**Kenapa bikin abstraction?**

Bayangkan kamu punya 100 test. Kalau base URL berubah, atau cara kirim token berubah, kamu nggak mau edit 100 file. Cukup edit di satu tempat: `ApiClient`. Ini namanya **Single Responsibility Principle**.

Perhatikan juga pattern `__enter__` dan `__exit__` -- ini supaya bisa dipakai dengan `with` statement, yang otomatis close connection setelah selesai.

---

### 1.4 Jalankan API Tests TypeScript

```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/api-tests/typescript
npm install        # Install dependencies (cuma sekali)
npx vitest run     # Jalankan semua tests
```

**Perbandingan Vitest (TypeScript) vs pytest (Python):**

| Aspek | pytest (Python) | Vitest (TypeScript) |
|-------|----------------|---------------------|
| Definisi test | `def test_xxx(self):` | `it('should xxx', async () => {})` |
| Assertion | `assert x == y` | `expect(x).toBe(y)` |
| Grouping | `class TestProducts:` | `describe('Products', () => {})` |
| Setup | `@pytest.fixture` | `beforeEach(async () => {})` |
| Schema validation | Pydantic | Zod |
| Menjalankan | `python -m pytest` | `npx vitest run` |

**Perbandingan Pydantic (Python) vs Zod (TypeScript):**

```python
# Python (Pydantic)
class Product(BaseModel):
    id: int
    title: str
    price: float
    brand: str | None = None
```

```typescript
// TypeScript (Zod)
const ProductSchema = z.object({
  id: z.number(),
  title: z.string(),
  price: z.number(),
  brand: z.string().optional(),
});
```

Konsepnya sama! Keduanya mendefinisikan "bentuk data yang diharapkan" dan otomatis validasi.

**Kenapa punya 2 bahasa?**
- Portfolio lebih kuat: menunjukkan kamu versatile
- Di interview: "Saya bisa Python DAN TypeScript"
- Realita industri: banyak company pakai salah satu, kamu siap keduanya

---

### 1.5 Postman Collection

File: `api-tests/postman/dummyjson.collection.json`

**Cara import ke Postman:**

1. Download & install Postman dari https://www.postman.com/downloads/
2. Buka Postman
3. Klik **"Import"** (tombol di kiri atas)
4. Pilih **"Upload Files"**
5. Navigate ke `api-tests/postman/dummyjson.collection.json`
6. Klik **"Import"**
7. Collection "DummyJSON" akan muncul di sidebar kiri
8. Klik tombol **"Run"** untuk jalankan semua request sekaligus

**Kenapa Postman masih relevan?**
- Manual testing & exploratory testing -- saat kamu belum tahu API-nya gimana
- Onboarding -- kirim collection ke tim baru, mereka langsung bisa coba
- Non-developer friendly -- QA Manual, PM, BA bisa pakai tanpa coding
- Quick debugging -- cek API response sebelum nulis automated test

---

### 1.6 Latihan Mandiri DAY 1

Setelah paham semua di atas, coba tantangan ini:

**Latihan 1: Tambah test baru untuk search products**
Buka `api-tests/tests/test_products.py` dan tambah test:
```python
def test_search_products_laptop(self, client: httpx.Client):
    response = client.get("/products/search", params={"q": "laptop"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["products"]) > 0
    # Pastikan semua result memang mengandung kata "laptop"
```

**Latihan 2: Coba break test dengan sengaja**
Ubah expected status code dan lihat error message:
```python
assert response.status_code == 500   # Sengaja salah, harusnya 200
```
Baca error message pytest -- itu skill penting! Kamu harus bisa baca log error.

**Latihan 3: Export Postman request sendiri**
Di Postman, buat request baru ke `GET https://dummyjson.com/products/search?q=laptop` dan export hasilnya.

**Latihan 4: Explore DummyJSON docs**
Buka https://dummyjson.com/docs dan coba endpoint yang belum di-test: `/users`, `/quotes`, `/recipes`.

---

## DAY 2: UI/E2E Testing + BDD

### 2.1 Pahami Dulu: Apa itu E2E Testing?

**E2E (End-to-End) Testing** = Testing dari sudut pandang user. Buka browser sungguhan, klik tombol, isi form, verifikasi hasilnya.

**Analogi:** Kamu jadi "robot user" yang mengetes aplikasi persis seperti user asli memakainya.

**Kenapa Playwright lebih baik dari Selenium?**

| Aspek | Playwright | Selenium |
|-------|-----------|----------|
| Auto-wait | Ya (otomatis tunggu element siap) | Tidak (harus manual WebDriverWait) |
| Speed | Sangat cepat | Lebih lambat |
| Setup | `pip install playwright` selesai | Perlu download WebDriver yang sesuai browser version |
| Network intercept | Built-in | Perlu tools tambahan |
| Multi-browser | Chromium, Firefox, WebKit (satu install) | Perlu driver terpisah per browser |
| Codegen | `playwright codegen` | Tidak ada |
| Trace viewer | Built-in | Tidak ada |

**Page Object Model (POM) -- simpelnya:**

Tanpa POM (kode berantakan):
```python
# Di test_login.py
page.locator("[data-test='username']").fill("standard_user")
page.locator("[data-test='password']").fill("secret_sauce")
page.locator("[data-test='login-button']").click()

# Di test_checkout.py -- nulis ulang hal yang sama!
page.locator("[data-test='username']").fill("standard_user")
page.locator("[data-test='password']").fill("secret_sauce")
page.locator("[data-test='login-button']").click()
```

Dengan POM (rapi, reusable):
```python
# Di pages/login_page.py -- definisi SEKALI
class LoginPage:
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

# Di test manapun -- pakai aja
login_page.login("standard_user", "secret_sauce")  # Satu baris!
```

Kalau UI berubah (misalnya locator berubah), kamu cuma perlu edit di SATU file page object.

---

### 2.2 Jalankan UI Tests Python

**Jalankan semua UI tests (headless -- tanpa browser terlihat):**
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground
python -m pytest ui-tests/python/tests/ -v
```

**Jalankan dengan browser terlihat (headed mode):**
```bash
python -m pytest ui-tests/python/tests/ -v --headed
```

Pakai `--headed` kalau kamu mau LIHAT apa yang browser lakukan. Ini sangat membantu saat debugging!

**Jalankan test spesifik:**
```bash
python -m pytest ui-tests/python/tests/test_login.py -v
python -m pytest ui-tests/python/tests/test_checkout_flow.py::TestCheckoutFlow::test_complete_checkout_single_item -v
```

**Pakai Playwright Codegen (super berguna buat belajar!):**
```bash
python -m playwright codegen https://www.saucedemo.com
```

Ini akan buka browser dan Playwright Inspector. Setiap kamu klik sesuatu di browser, Playwright otomatis generate kode-nya! Ini cara paling gampang buat:
- Belajar locator yang benar
- Prototyping test baru
- Memahami flow user

---

### 2.3 Pelajari Kode UI Test

#### File: `ui-tests/python/pages/base_page.py` -- Fondasi Page Object

```python
class BasePage:
    def __init__(self, page):
        self.page = page                    # Playwright Page object

    def navigate(self, url: str):
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)

    def wait_for_url(self, url_pattern: str):
        with allure.step(f"Wait for URL to match: {url_pattern}"):
            self.page.wait_for_url(url_pattern)

    def screenshot(self, name: str):
        screenshot_bytes = self.page.screenshot()
        allure.attach(screenshot_bytes, name=name,
                      attachment_type=allure.attachment_type.PNG)
```

**Kenapa ada BasePage?**
Semua page object (LoginPage, InventoryPage, CartPage, CheckoutPage) inherit dari BasePage. Ini artinya:
- Semua page bisa `navigate()`, `wait_for_url()`, `screenshot()` tanpa nulis ulang
- Kalau mau tambah fitur umum (misalnya logging), cukup tambah di BasePage
- Ini namanya **inheritance** -- konsep OOP yang sering ditanya di interview

---

#### File: `ui-tests/python/pages/login_page.py` -- Locator Strategy

```python
class LoginPage(BasePage):
    URL = "https://www.saucedemo.com"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        self.error_message.wait_for(state="visible")
        return self.error_message.text_content()
```

**Locator strategy priority (urutan terbaik):**

1. **Role** -- `page.get_by_role("button", name="Login")` -- Paling stabil, accessibility-based
2. **Test ID** -- `page.locator("[data-test='login-button']")` -- Dibuat khusus untuk testing
3. **Label** -- `page.get_by_label("Username")` -- Berdasarkan label form
4. **Text** -- `page.get_by_text("Submit")` -- Berdasarkan text content
5. **CSS Selector** -- `page.locator(".btn-primary")` -- Bisa berubah saat redesign

Di Sauce Demo, kita pakai `data-test` attribute karena memang sudah disediakan oleh developer khusus untuk testing. Ini best practice: developer menambahkan `data-test` attribute supaya locator stabil dan nggak berubah walau UI di-redesign.

---

#### File: `ui-tests/python/pages/inventory_page.py` -- Complex Page Object

```python
class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.product_items = page.locator("[data-test='inventory-item']")
        self.product_names = page.locator("[data-test='inventory-item-name']")
        self.product_prices = page.locator("[data-test='inventory-item-price']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")

    def add_product_to_cart(self, product_name: str):
        product_item = self.page.locator(
            "[data-test='inventory-item']",
            has=self.page.locator("[data-test='inventory-item-name']",
                                  has_text=product_name),
        )
        product_item.locator("button", has_text="Add to cart").click()

    def get_product_prices(self) -> list[float]:
        raw_prices = self.product_prices.all_text_contents()
        return [float(price.replace("$", "")) for price in raw_prices]

    def sort_products(self, option_value: str):
        self.sort_dropdown.select_option(option_value)
```

**Perhatikan pattern `has` dan `has_text`:**

```python
product_item = self.page.locator(
    "[data-test='inventory-item']",                              # Parent element
    has=self.page.locator("[data-test='inventory-item-name']",   # Yang mengandung child
                          has_text=product_name),                # Dengan text tertentu
)
product_item.locator("button", has_text="Add to cart").click()   # Klik tombol di dalamnya
```

Ini cara Playwright yang elegant untuk bilang: "Cari product card yang nama-nya 'Sauce Labs Backpack', lalu klik tombol Add to cart di dalam card itu." Jauh lebih readable daripada XPath yang panjang dan sulit dibaca.

---

#### File: `ui-tests/python/tests/conftest.py` -- Browser Fixtures

```python
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def browser_context(browser):
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def logged_in_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(STANDARD_USER, PASSWORD)
    page.wait_for_url("**/inventory.html")
    return page
```

**Hirarki fixture yang penting dipahami:**

```
Browser (session) -- satu browser untuk semua test
  |
  +-- Context (function) -- "incognito window" baru per test
        |
        +-- Page (function) -- tab browser baru per test
              |
              +-- logged_in_page -- page yang sudah login
```

**Kenapa `browser` scope-nya `session`?**
Karena launch browser itu mahal (butuh waktu). Kita cuma launch SEKALI untuk seluruh session.

**Kenapa `context` scope-nya `function`?**
Karena setiap test harus mulai dari keadaan bersih. Context itu seperti "incognito window" -- cookies, storage, semua di-reset. Jadi test A nggak pengaruh ke test B.

**`logged_in_page` -- fixture yang sudah login:**
Banyak test butuh user yang sudah login. Daripada setiap test login sendiri, kita bikin fixture yang otomatis login dan return page yang sudah di inventory.

---

#### File: `ui-tests/python/tests/test_checkout_flow.py` -- Full E2E Flow

```python
def test_complete_checkout_single_item(self, logged_in_page):
    page = logged_in_page

    # Step 1: Add product to cart
    inventory_page = InventoryPage(page)
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    assert inventory_page.get_cart_badge_count() == 1

    # Step 2: Go to cart and verify
    inventory_page.go_to_cart()
    cart_page = CartPage(page)
    assert "Sauce Labs Backpack" in cart_page.get_cart_items()

    # Step 3: Proceed to checkout
    cart_page.proceed_to_checkout()

    # Step 4: Fill information
    checkout_page = CheckoutPage(page)
    checkout_page.fill_information("John", "Doe", "12345")
    checkout_page.continue_checkout()

    # Step 5: Finish order
    checkout_page.finish_checkout()

    # Step 6: Verify confirmation
    confirmation = checkout_page.get_confirmation_message()
    assert "Thank you for your order" in confirmation
```

**Lihat betapa bersihnya kode ini!** Berkat Page Object Model, test ini terbaca seperti cerita:
1. Tambah Sauce Labs Backpack ke keranjang
2. Buka keranjang, pastikan item ada
3. Lanjut ke checkout
4. Isi data diri
5. Selesaikan pesanan
6. Pastikan muncul pesan konfirmasi

Bandingkan kalau tanpa POM -- akan penuh dengan `page.locator(...)` di mana-mana.

---

### 2.4 Jalankan UI Tests TypeScript

```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/ui-tests/typescript

# Install (pertama kali)
npm install
npx playwright install chromium

# Jalankan tests (headless)
npx playwright test --project=chromium

# Jalankan tests (dengan browser terlihat)
npx playwright test --headed

# Lihat HTML report
npx playwright show-report
```

HTML report dari Playwright itu sangat informatif -- ada screenshot on failure, trace, dan timeline.

**Perbandingan Python vs TypeScript Playwright:**

```python
# Python
login_page = LoginPage(page)
login_page.open()
login_page.login("standard_user", "secret_sauce")
page.wait_for_url("**/inventory.html")
```

```typescript
// TypeScript
const loginPage = new LoginPage(page);
await loginPage.goto();
await loginPage.login('standard_user', 'secret_sauce');
await expect(page).toHaveURL(/.*inventory.html/);
```

Hampir sama! Perbedaan utama:
- TypeScript pakai `await` (async by default)
- TypeScript pakai `expect(page).toHaveURL(regex)` yang auto-waits
- Python pakai `page.wait_for_url(pattern)` yang explicit

**Multi-browser testing di TypeScript:**
```bash
npx playwright test                # Jalankan di SEMUA browser (Chromium, Firefox, WebKit)
npx playwright test --project=firefox
npx playwright test --project=webkit
```

Ini possible karena `playwright.config.ts` sudah setup 3 project: chromium, firefox, webkit.

---

### 2.5 BDD dengan Gherkin

**Apa itu BDD?**

BDD (Behavior-Driven Development) adalah cara menulis test yang bisa dibaca oleh SEMUA orang -- developer, QA, PM, bahkan klien. Pakai bahasa natural: Given-When-Then.

**Kenapa enterprise/perusahaan besar suka BDD?**
- PM bisa baca dan validasi test scenario tanpa bisa coding
- Jadi living documentation -- test = dokumentasi
- Membantu komunikasi antara tim teknis dan non-teknis
- Sering diminta di job posting QA

#### File: `bdd/features/login.feature` -- Gherkin Feature File

```gherkin
Feature: User Login
  As a user
  I want to log in to Sauce Demo
  So that I can access the inventory

  @smoke @critical
  Scenario: Successful login with standard user
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page

  @negative
  Scenario: Login fails with locked out user
    Given I am on the login page
    When I login with username "locked_out_user" and password "secret_sauce"
    Then I should see error message "Sorry, this user has been locked out"
```

**Penjelasan sintaks Gherkin:**
- `Feature:` -- Deskripsi fitur yang ditest
- `As a ... I want ... So that ...` -- User story (siapa, mau apa, kenapa)
- `Scenario:` -- Satu skenario test
- `Given` -- Kondisi awal (setup)
- `When` -- Aksi yang dilakukan
- `Then` -- Hasil yang diharapkan (assertion)
- `@smoke`, `@negative` -- Tag untuk filter test

#### File: `bdd/features/checkout.feature` -- Dengan Background

```gherkin
Feature: Checkout Process

  Background:
    Given I am logged in as "standard_user"
    And I have added "Sauce Labs Backpack" to the cart

  Scenario: Complete checkout with valid information
    When I go to the cart
    And I proceed to checkout
    And I fill in first name "John" and last name "Doe" and postal code "12345"
    And I continue to the overview
    And I finish the order
    Then I should see the order confirmation message "Thank you for your order!"
```

**`Background`** = steps yang dijalankan SEBELUM setiap Scenario di feature file ini. Semua scenario di sini mulai dari kondisi "sudah login dan sudah add item ke cart".

#### File: `bdd/steps/test_login.py` -- Step Definitions

```python
from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import Page, expect

scenarios('../features/login.feature')    # Connect ke feature file

@given('I am on the login page')
def navigate_to_login(page: Page):
    page.goto('https://www.saucedemo.com/')

@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def login_with_credentials(page: Page, username: str, password: str):
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()

@then('I should be redirected to the inventory page')
def verify_inventory_page(page: Page):
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html')
```

**Cara kerjanya:**
1. Feature file bilang: `Given I am on the login page`
2. pytest-bdd cari function yang di-decorate `@given('I am on the login page')`
3. Ketemu `navigate_to_login()`, jalankan!
4. `parsers.parse(...)` bisa extract parameter dari teks: `"{username}"` jadi parameter `username`

**Jalankan BDD tests:**
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground
python -m pytest bdd/ -v
```

---

### 2.6 Latihan Mandiri DAY 2

**Latihan 1: Buat page object baru**
Coba bikin page object untuk "Product Detail" page di Sauce Demo. Hint: klik salah satu product di inventory page, lalu bikin page object untuk halaman itu.

**Latihan 2: Tulis Gherkin scenario baru**
Tambah scenario di `bdd/features/product_search.feature`:
```gherkin
Scenario: Sort products by price high to low
  When I sort products by "Price (high to low)"
  Then the products should be sorted by price descending
```
Lalu buat step definition-nya di `bdd/steps/test_product_search.py`.

**Latihan 3: Pakai Playwright Codegen**
```bash
python -m playwright codegen https://www.saucedemo.com
```
Record flow: login -> add 2 items -> go to cart -> remove 1 item -> checkout. Lihat kode yang di-generate, bandingkan dengan Page Object yang sudah ada.

**Latihan 4: Cross-browser testing**
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/ui-tests/typescript
npx playwright test               # Jalankan di semua browser
```
Lihat apakah ada test yang pass di Chromium tapi fail di Firefox/WebKit.

---

## DAY 3: Load Testing + Polish

### 3.1 Pahami Dulu: Apa itu Load Testing?

Load testing = test seberapa kuat server/aplikasi kamu saat dipakai banyak orang sekaligus.

**5 Tipe Load Testing:**

| Tipe | Tujuan | Analogi |
|------|--------|---------|
| **Smoke** | Cek apakah server bisa handle traffic minimal | 1 orang masuk toko |
| **Load** | Cek performa di kondisi normal | 100 orang belanja normal |
| **Stress** | Cari breaking point server | Terus tambah orang sampai toko penuh sesak |
| **Spike** | Cek apakah server survive traffic mendadak | Flash sale -- 0 ke 10.000 orang dalam 1 menit |
| **Soak** | Cek apakah server stabil dalam waktu lama | Toko buka 24 jam non-stop selama seminggu |

**Key Metrics yang harus dipahami:**

| Metrik | Artinya | Target Umum |
|--------|---------|-------------|
| **RPS** (Requests Per Second) | Berapa request yang bisa diproses per detik | Tergantung app |
| **P95 Latency** | 95% request selesai dalam waktu ini | < 500ms |
| **P99 Latency** | 99% request selesai dalam waktu ini | < 1000ms |
| **Error Rate** | Persentase request yang gagal | < 1% |
| **Throughput** | Total data yang ditransfer per detik | Tergantung app |

**Kenapa P95, bukan Average?**
Average bisa menyesatkan. Kalau 99 request selesai dalam 10ms dan 1 request butuh 10 detik, average-nya 110ms -- terlihat baik. Tapi P99 akan menunjukkan 10 detik -- ada masalah!

---

### 3.2 Jalankan k6

**Install k6:**
- Download dari https://k6.io/docs/get-started/installation/
- Windows: `winget install k6` atau download binary

**Jalankan Smoke Test:**
```bash
k6 run C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/load-tests/k6/scenarios/smoke.js
```

**Jalankan Load Test:**
```bash
k6 run C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/load-tests/k6/scenarios/load.js
```

**Jalankan Stress Test:**
```bash
k6 run C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/load-tests/k6/scenarios/stress.js
```

**Cara baca output k6:**

```
     checks.........................: 100.00% ---- semua check pass
     data_received..................: 1.2 MB  ---- total data diterima
     data_sent......................: 54 kB   ---- total data dikirim
     http_req_blocked...............: avg=2ms  ---- waktu tunggu koneksi
     http_req_duration..............: avg=120ms p(95)=250ms ---- INI YANG PENTING!
     http_req_failed................: 0.00%   ---- nggak ada request gagal
     iterations.....................: 30       ---- berapa kali loop dijalankan
     vus............................: 10       ---- virtual users aktif
```

Yang paling penting dilihat:
- `http_req_duration p(95)` -- Harus di bawah threshold (di kode: `p(95)<500`)
- `http_req_failed` -- Harus mendekati 0%
- `checks` -- Semua check harus 100%

---

#### File: `load-tests/k6/scenarios/smoke.js` -- Anatomy

```javascript
export const options = {
  vus: 1,                                    // 1 virtual user
  duration: '1m',                            // Selama 1 menit
  thresholds: {
    http_req_duration: ['p(95)<500'],         // 95% request harus < 500ms
    http_req_failed: ['rate<0.01'],           // Error rate harus < 1%
  },
};

export default function () {
  // Test 1: Login
  const loginRes = http.post(`${BASE_URL}/auth/login`, loginPayload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(loginRes, {
    'login status is 200': (r) => r.status === 200,
    'login returns token': (r) => JSON.parse(r.body).accessToken !== undefined,
  });
  sleep(1);     // Simulasi "thinking time" user

  // Test 2: Browse products
  const productsRes = http.get(`${BASE_URL}/products?limit=10`);
  check(productsRes, {
    'products status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
```

**Penjelasan:**
- `vus: 1` -- Cuma 1 user. Ini smoke test, tujuannya cek apakah server jalan, bukan stress test.
- `thresholds` -- Kalau P95 > 500ms atau error rate > 1%, test GAGAL.
- `check()` -- Validasi response (mirip assert tapi nggak stop execution).
- `sleep(1)` -- Simulasi user yang pause 1 detik antara aksi (realistic behavior).

---

#### File: `load-tests/k6/scenarios/checkout_load.js` -- Advanced k6

```javascript
// Custom metrics -- kita bisa track metrik spesifik!
const loginDuration = new Trend('login_duration');
const checkoutDuration = new Trend('checkout_duration');
const checkoutSuccessRate = new Rate('checkout_success_rate');
const totalCheckouts = new Counter('total_checkouts');

export const options = {
  stages: [
    { duration: '30s', target: 5 },       // Ramp up ke 5 users
    { duration: '2m', target: 10 },        // Hold di 10 users selama 2 menit
    { duration: '30s', target: 0 },        // Ramp down ke 0
  ],
  thresholds: {
    login_duration: ['p(95)<400'],          // Login harus < 400ms
    checkout_duration: ['p(95)<600'],       // Checkout harus < 600ms
    checkout_success_rate: ['rate>0.95'],   // 95% checkout harus sukses
  },
};

export default function () {
  // Pakai group() untuk organisasi di report
  group('01_Authentication', function () {
    const loginRes = http.post(...);
    loginDuration.add(loginRes.timings.duration);  // Track custom metric
  });

  group('02_Browse_Products', function () { ... });
  group('03_Add_To_Cart', function () { ... });
  group('04_Checkout', function () {
    checkoutDuration.add(checkoutRes.timings.duration);
    totalCheckouts.add(1);
    checkoutSuccessRate.add(checkoutRes.status === 200);
  });
}
```

**Advanced concepts:**
- **Stages** -- Simulasi traffic pattern: naik pelan, hold, turun pelan
- **Custom metrics** -- Track hal spesifik selain default metrics
- **Groups** -- Organisasi test dalam kelompok yang bisa dilihat terpisah di report
- **Trend/Rate/Counter** -- 3 tipe custom metric (durasi, persentase, hitungan)

---

### 3.3 Jalankan Locust

**Jalankan Locust:**
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground
python -m locust -f load-tests/locust/locustfile.py --host=https://dummyjson.com
```

**Buka dashboard di browser:**
```
http://localhost:8089
```

**Setting di web UI:**
- Number of users: `10` (berapa virtual user)
- Spawn rate: `2` (berapa user baru per detik)
- Klik **Start Swarming**

**Dashboard Locust menampilkan:**
- Real-time RPS (requests per second)
- Response time graph
- Failure rate
- Per-endpoint breakdown

---

#### File: `load-tests/locust/locustfile.py` -- Penjelasan

```python
from locust import HttpUser, task, between

class ShopUser(HttpUser):
    host = "https://dummyjson.com"
    wait_time = between(1, 3)        # Pause 1-3 detik antara aksi (random)

    def on_start(self):
        """Dijalankan SEKALI saat user mulai (login)."""
        response = self.client.post("/auth/login", json={
            "username": "emilys", "password": "emilyspass",
        })
        self.token = response.json().get("accessToken", "")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)                          # Weight 3 -- 3x lebih sering dipanggil
    def browse_products(self):
        self.client.get("/products?limit=10", headers=self.headers)

    @task(2)                          # Weight 2
    def view_product(self):
        product_id = random.randint(1, 30)
        self.client.get(f"/products/{product_id}", headers=self.headers)

    @task(1)                          # Weight 1 -- paling jarang
    def add_to_cart(self):
        payload = {"userId": 1, "products": [{"id": 1, "quantity": 1}]}
        self.client.post("/carts/add", json=payload, headers=self.headers)

    @task(1)
    def search_products(self):
        term = random.choice(["phone", "laptop", "watch", "shirt"])
        self.client.get(f"/products/search?q={term}", headers=self.headers)
```

**Penjelasan `@task` weights:**
- `@task(3)` browse_products: dipanggil 3 kali per "cycle"
- `@task(2)` view_product: dipanggil 2 kali per "cycle"
- `@task(1)` add_to_cart: dipanggil 1 kali per "cycle"

Total weight = 3+2+1+1 = 7. Jadi browse_products dipanggil 3/7 = 43% dari waktu. Ini realistic karena di dunia nyata, user lebih sering browsing daripada checkout.

**k6 vs Locust:**

| Aspek | k6 | Locust |
|-------|-----|--------|
| Bahasa | JavaScript | Python |
| Dashboard | CLI output (atau Grafana) | Web UI built-in |
| CI/CD friendly | Sangat (exit code) | Kurang (butuh headless mode) |
| Coding style | Scripting | OOP (class-based) |
| Terbaik untuk | CI/CD pipeline | Exploratory load testing, demo ke stakeholder |

---

### 3.4 Allure Reports

**Install Allure CLI:**
- Download dari https://allurereport.org/docs/install/
- Atau: `npm install -g allure-commandline`

**Generate dan lihat report:**
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground

# Step 1: Jalankan tests dengan output Allure
python -m pytest api-tests/tests/ --alluredir=reports/allure-results -v -p no:playwright

# Step 2: Buka report di browser
allure serve reports/allure-results
```

**Apa yang kamu lihat di Allure report:**
- **Overview** -- Ringkasan: berapa pass, fail, broken, skipped
- **Suites** -- Grouped by class/module
- **Graphs** -- Trend, duration, severity distribution
- **Categories** -- Grouped by `@allure.epic`, `@allure.feature`, `@allure.story`
- **Timeline** -- Kapan setiap test jalan, berapa lama
- **Behaviors** -- Grouped by epic > feature > story
- **Severity** -- BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL

**Kenapa Allure penting untuk portfolio?**
- Screenshot report yang bagus di portfolio = nilai plus BESAR
- Menunjukkan kamu nggak cuma bisa nulis test, tapi juga bisa present result
- Di real company, stakeholder/PM melihat report -- bukan kode

---

### 3.5 CI/CD Pipeline

#### File: `.github/workflows/test-pipeline.yml` -- Penjelasan

```yaml
name: QA Automation Pipeline

on:
  push:
    branches: [main, develop]    # Jalan saat push ke main atau develop
  pull_request:
    branches: [main]             # Jalan saat buat PR ke main
```

**Trigger:** Pipeline ini jalan otomatis saat kamu push code atau buat pull request. Kamu nggak perlu manually jalankan apa-apa.

**Jobs yang jalan PARALEL:**

```
+------------------+     +-------------------+     +--------------------+
| api-tests        |     | api-tests-ts      |     | ui-tests-python    |
| (Python pytest)  |     | (TypeScript Vitest)|    | (Python Playwright)|
+------------------+     +-------------------+     +--------------------+
        |                         |                          |
+------------------+     +-------------------+     +--------------------+
| ui-tests-ts      |     | bdd-tests         |     | load-tests         |
| (TS Playwright)  |     | (pytest-bdd)      |     | (k6 smoke)         |
+------------------+     +-------------------+     +--------------------+
```

Semua 6 job jalan BERSAMAAN (parallel) -- ini bikin pipeline cepat. Kalau sequential, bisa 20+ menit. Parallel bisa selesai dalam 5-7 menit.

**Setiap job melakukan:**

1. **api-tests** -- Install Python, install packages, jalankan smoke tests dulu, lalu semua tests, upload Allure results
2. **api-tests-ts** -- Install Node.js, npm install, jalankan vitest
3. **ui-tests-python** -- Install Python + Playwright + browser, jalankan UI tests, upload Allure results
4. **ui-tests-ts** -- Install Node.js + Playwright + browser, jalankan tests, upload Playwright report
5. **bdd-tests** -- Install Python + Playwright + browser, jalankan BDD tests, upload Allure results
6. **load-tests** -- Install k6, jalankan smoke test

**Artifacts:** Setelah pipeline selesai, kamu bisa download report dari GitHub Actions page. Ini berguna untuk debugging kalau test gagal di CI tapi pass di local.

**Cara cek pipeline status:**
1. Push code ke GitHub
2. Buka repository di GitHub
3. Klik tab **"Actions"**
4. Lihat workflow run terbaru
5. Klik untuk lihat detail setiap job
6. Download artifacts (report) kalau perlu

---

### 3.6 Latihan Mandiri DAY 3

**Latihan 1: Modifikasi k6 thresholds**
Buka `load-tests/k6/scenarios/smoke.js` dan ubah threshold:
```javascript
thresholds: {
  http_req_duration: ['p(95)<50'],    // 50ms -- hampir pasti gagal!
}
```
Jalankan dan lihat apa yang terjadi saat threshold terlanggar.

**Latihan 2: Tambah Locust task baru**
Buka `load-tests/locust/locustfile.py` dan tambah task:
```python
@task(1)
def get_categories(self):
    self.client.get("/products/categories", headers=self.headers,
                    name="/products/categories")
```

**Latihan 3: Generate full Allure report**
Jalankan SEMUA tests dan generate report:
```bash
python -m pytest api-tests/tests/ ui-tests/python/tests/ bdd/ --alluredir=reports/allure-results -v
allure serve reports/allure-results
```
Screenshot hasilnya dan simpan untuk portfolio!

**Latihan 4: Push ke GitHub dan lihat CI/CD**
```bash
git add .
git commit -m "feat: add new tests and learning exercises"
git push origin main
```
Buka GitHub Actions dan lihat pipeline jalan.

---

## Tips Interview QA

### Q1: Kenapa pilih Playwright, bukan Selenium?

**Jawaban:**

"Saya pilih Playwright karena beberapa alasan teknis:

Pertama, **auto-wait**. Di Selenium, kita harus manual nambahkan WebDriverWait atau sleep untuk tunggu element muncul. Di Playwright, semua action otomatis menunggu element ready -- ini mengurangi flaky test secara signifikan.

Kedua, **setup yang lebih simpel**. Di Selenium, kita harus download WebDriver yang sesuai dengan versi browser, dan sering error kalau browser update. Di Playwright, cukup `playwright install chromium` dan selesai.

Ketiga, **fitur bawaan yang powerful**: network interception, codegen untuk recording, trace viewer untuk debugging, dan multi-browser support dalam satu framework.

Keempat, **performa**. Playwright berkomunikasi langsung dengan browser via CDP (Chrome DevTools Protocol) yang lebih cepat dibandingkan Selenium WebDriver protocol.

Tapi saya juga paham Selenium -- banyak project legacy yang masih pakai Selenium, dan konsep dasarnya sama: locator, wait, assertion."

---

### Q2: Apa bedanya Load Test, Stress Test, dan Spike Test?

**Jawaban:**

"Ketiganya punya tujuan berbeda:

**Load Test** -- Menguji performa di kondisi traffic NORMAL. Misalnya, aplikasi e-commerce kita biasanya melayani 500 concurrent users. Load test simulasikan 500 users dan pastikan response time tetap acceptable (misalnya P95 < 500ms). Tujuannya: pastikan SLA terpenuhi.

**Stress Test** -- Menguji BATAS KEMAMPUAN sistem. Kita terus naikkan traffic melampaui kapasitas normal -- 500, 1000, 2000, 5000 users -- sampai sistem mulai degradasi atau crash. Tujuannya: tahu breaking point dan bagaimana sistem recover setelah overload.

**Spike Test** -- Menguji kemampuan sistem menangani LONJAKAN MENDADAK. Misalnya, dari 100 users langsung naik ke 10.000 users dalam waktu singkat (simulasi flash sale atau viral moment). Tujuannya: pastikan sistem bisa survive sudden traffic spike dan recover dengan cepat.

Di project saya, saya implementasikan ketiganya menggunakan k6 dengan stages configuration yang berbeda -- smoke dengan 1 VU, load dengan ramp up ke 10 VU, dan stress dengan ramp up bertahap sampai 100 VU."

---

### Q3: Apa itu Page Object Model dan kenapa penting?

**Jawaban:**

"Page Object Model (POM) adalah design pattern di UI testing di mana setiap halaman web direpresentasikan sebagai sebuah class. Class itu berisi locator (element) dan method (aksi yang bisa dilakukan di halaman tersebut).

Kenapa penting:

**Pertama, maintainability.** Kalau UI berubah -- misalnya tombol login pindah atau id-nya berubah -- saya cuma perlu update di SATU file page object. Tanpa POM, saya harus update di semua test file yang pakai element itu.

**Kedua, readability.** Test yang pakai POM terbaca seperti cerita: `login_page.login(user, pass)`, `inventory_page.add_to_cart('Backpack')`, `cart_page.checkout()`. Tanpa POM, test penuh dengan `page.locator('[data-test=xxx]').click()` yang susah dibaca.

**Ketiga, reusability.** Method `login()` di LoginPage bisa dipakai di semua test yang perlu login. DRY principle.

Di project saya, saya implementasikan POM dengan inheritance pattern: BasePage sebagai parent class yang punya method umum (navigate, screenshot, wait), lalu LoginPage, InventoryPage, CartPage, CheckoutPage yang extend BasePage."

---

### Q4: Apa benar GraphQL selalu return HTTP 200? Gimana handle error-nya?

**Jawaban:**

"Ya, ini perbedaan fundamental antara REST dan GraphQL. Di REST, error dikomunikasikan lewat HTTP status code: 404 Not Found, 401 Unauthorized, 500 Internal Server Error.

Di GraphQL, server hampir SELALU mengembalikan HTTP 200 OK -- bahkan ketika ada error. Error-nya ada di response body, dalam field `errors`:

```json
{
  \"data\": null,
  \"errors\": [
    {
      \"message\": \"Cannot query field 'nonExistentField'\",
      \"locations\": [{\"line\": 2, \"column\": 3}]
    }
  ]
}
```

Jadi dalam testing GraphQL, saya tidak cukup hanya cek `response.status_code == 200`. Saya juga harus parsing response body dan:
1. Cek apakah ada field `errors` -- kalau ada, berarti ada masalah
2. Cek apakah field `data` berisi data yang expected atau null
3. Validasi schema dari data yang dikembalikan

Di project saya, saya punya test yang membuktikan ini: mengirim query yang invalid dan memverifikasi bahwa HTTP status tetap 200, tapi response body mengandung `errors`."

---

### Q5: Metrik paling penting di load testing itu apa?

**Jawaban:**

"Menurut saya, metrik yang paling penting adalah **P95/P99 latency** dan **error rate**. Ini alasannya:

**P95 latency** lebih penting dari average karena average bisa menyembunyikan masalah. Kalau 1000 request, 990 selesai dalam 50ms, tapi 10 request butuh 30 detik -- average-nya tetap terlihat bagus (350ms). Tapi P99 akan menunjukkan 30 detik -- itu berarti 1% user mengalami timeout. P95 artinya 95% user mendapat response time di bawah angka itu.

**Error rate** penting karena seberapa cepat pun server merespons, kalau 5% request gagal, itu masalah serius. Di e-commerce, 5% error rate berarti 5 dari 100 user gagal checkout -- itu lost revenue.

Selain itu, saya juga memperhatikan:
- **Throughput (RPS)** -- berapa request per second yang bisa di-handle
- **Connection time** -- waktu untuk establish connection (bisa indikasi server kewalahan)
- **Custom metrics** -- di project saya, saya track `login_duration`, `checkout_duration`, dan `checkout_success_rate` secara terpisah supaya bisa pinpoint bottleneck spesifik.

Di k6, semua ini bisa didefinisikan sebagai thresholds yang otomatis fail kalau dilanggar -- sangat berguna di CI/CD pipeline."

---

## Cheat Sheet: Semua Command

### Setup (Pertama Kali)
```bash
# Virtual environment
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground
python -m venv venv
source venv/Scripts/activate

# Python packages
pip install httpx pydantic pytest allure-pytest pytest-bdd playwright locust

# Playwright browser
python -m playwright install chromium

# Node.js packages - API tests
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/api-tests/typescript
npm install

# Node.js packages - UI tests
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/ui-tests/typescript
npm install
npx playwright install chromium
```

### API Tests (DAY 1)
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground

# Semua API tests Python
python -m pytest api-tests/tests/ -v -p no:playwright

# Test spesifik
python -m pytest api-tests/tests/test_auth.py -v -p no:playwright
python -m pytest api-tests/tests/test_auth.py::TestAuth::test_login_valid_credentials -v -p no:playwright

# By marker
python -m pytest api-tests/tests/ -m smoke -v -p no:playwright
python -m pytest api-tests/tests/ -m regression -v -p no:playwright
python -m pytest api-tests/tests/ -m negative -v -p no:playwright

# API tests TypeScript
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/api-tests/typescript
npx vitest run
```

### UI Tests (DAY 2)
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground

# UI tests Python (headless)
python -m pytest ui-tests/python/tests/ -v

# UI tests Python (with browser visible)
python -m pytest ui-tests/python/tests/ -v --headed

# Playwright Codegen (record browser actions)
python -m playwright codegen https://www.saucedemo.com

# UI tests TypeScript
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/ui-tests/typescript
npx playwright test --project=chromium
npx playwright test --headed
npx playwright show-report

# BDD tests
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground
python -m pytest bdd/ -v
```

### Load Tests (DAY 3)
```bash
# k6
k6 run C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/load-tests/k6/scenarios/smoke.js
k6 run C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/load-tests/k6/scenarios/load.js
k6 run C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/load-tests/k6/scenarios/stress.js
k6 run C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/load-tests/k6/scenarios/checkout_load.js

# Locust (opens web UI at http://localhost:8089)
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground
python -m locust -f load-tests/locust/locustfile.py --host=https://dummyjson.com
```

### Reports
```bash
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground

# Generate Allure results
python -m pytest api-tests/tests/ --alluredir=reports/allure-results -v -p no:playwright

# View Allure report (opens browser)
allure serve reports/allure-results

# Playwright HTML report
cd C:/Users/Admin/Pictures/Learne2e/qa-automation-playground/ui-tests/typescript
npx playwright show-report
```

### Git & CI/CD
```bash
git status
git add .
git commit -m "feat: description of changes"
git push origin main
# Then check GitHub Actions tab for pipeline status
```

---

## Struktur Folder Lengkap

```
qa-automation-playground/
|
|-- api-tests/
|   |-- conftest.py              # Fixtures: base_url, auth_token, client
|   |-- clients/
|   |   |-- api_client.py        # HTTP client abstraction
|   |-- models/
|   |   |-- product.py           # Pydantic: Product, ProductsResponse
|   |   |-- user.py              # Pydantic: LoginResponse
|   |   |-- cart.py              # Pydantic: Cart, CartProduct
|   |-- tests/
|   |   |-- test_products.py     # 14 tests: CRUD, search, pagination, schema
|   |   |-- test_auth.py         # 7 tests: login, token, protected endpoints
|   |   |-- test_graphql.py      # 6 tests: Countries API, error handling
|   |   |-- test_cart.py         # 6 tests: cart CRUD, schema
|   |-- typescript/
|   |   |-- products.test.ts     # Vitest + Zod: 5 tests
|   |-- postman/
|       |-- dummyjson.collection.json
|
|-- ui-tests/
|   |-- python/
|   |   |-- data/users.py        # Test data: usernames, passwords
|   |   |-- pages/
|   |   |   |-- base_page.py     # BasePage: navigate, screenshot
|   |   |   |-- login_page.py    # LoginPage: login, get_error
|   |   |   |-- inventory_page.py # InventoryPage: add_to_cart, sort
|   |   |   |-- cart_page.py     # CartPage: get_items, remove, checkout
|   |   |   |-- checkout_page.py # CheckoutPage: fill_info, finish
|   |   |-- components/
|   |   |   |-- cart_icon.py     # Reusable cart icon component
|   |   |-- tests/
|   |       |-- conftest.py      # Browser fixtures: browser, context, page
|   |       |-- test_login.py    # 5 tests: login scenarios
|   |       |-- test_inventory.py # 5 tests: products, sort, cart badge
|   |       |-- test_checkout_flow.py # 4 tests: full E2E checkout
|   |-- typescript/
|       |-- playwright.config.ts # Multi-browser config
|       |-- pages/
|       |   |-- login-page.ts    # LoginPage (TypeScript)
|       |   |-- inventory-page.ts # InventoryPage (TypeScript)
|       |-- tests/
|           |-- login.spec.ts    # Login tests (TypeScript)
|           |-- inventory.spec.ts # Inventory tests (TypeScript)
|           |-- checkout.spec.ts # Checkout tests (TypeScript)
|
|-- bdd/
|   |-- conftest.py              # Browser fixtures + shared Given steps
|   |-- features/
|   |   |-- login.feature        # 3 scenarios: login success/fail
|   |   |-- product_search.feature # 3 scenarios: view, sort
|   |   |-- checkout.feature     # 3 scenarios: checkout success/fail
|   |-- steps/
|       |-- test_login.py        # Step definitions for login
|       |-- test_product_search.py # Step definitions for product browsing
|       |-- test_checkout.py     # Step definitions for checkout
|
|-- load-tests/
|   |-- k6/
|   |   |-- scenarios/
|   |   |   |-- smoke.js         # 1 VU, 1 min (sanity check)
|   |   |   |-- load.js          # 10 VU, ramp up/down (normal load)
|   |   |   |-- stress.js        # 10->50->100 VU (find breaking point)
|   |   |   |-- checkout_load.js # Custom metrics, groups (e-commerce flow)
|   |   |-- thresholds.js        # Reusable threshold configs
|   |-- locust/
|       |-- locustfile.py        # Python load test with web UI
|
|-- .github/
|   |-- workflows/
|       |-- test-pipeline.yml    # 6 parallel CI/CD jobs
|
|-- reports/                     # Generated test reports (gitignored)
|-- LEARNING_GUIDE.md            # <-- Kamu di sini!
|-- README.md
|-- TEST_STRATEGY.md
|-- CONTRIBUTING.md
```

---

## Penutup

Selamat! Kalau kamu sudah sampai sini dan sudah jalankan semua command di atas, kamu sudah punya:

1. **API Testing** -- Python (pytest + httpx + Pydantic + Allure) + TypeScript (Vitest + Zod)
2. **UI/E2E Testing** -- Python Playwright + TypeScript Playwright + Page Object Model
3. **BDD** -- pytest-bdd + Gherkin feature files
4. **Load Testing** -- k6 (JavaScript) + Locust (Python)
5. **CI/CD** -- GitHub Actions pipeline
6. **Reporting** -- Allure + Playwright HTML reports

Ini bukan portfolio biasa. Ini menunjukkan kamu paham **testing pyramid**, **multiple languages**, **multiple tools**, dan **real-world patterns**. Good luck di interview!
