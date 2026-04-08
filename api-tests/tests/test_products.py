import allure
import httpx
import pytest

from models.product import Product, ProductsResponse


@allure.epic("E-Commerce API")
@allure.feature("Products")
class TestProducts:
    """Tests for the /products endpoints."""

    @allure.story("List Products")
    @allure.title("GET /products returns 200")
    @pytest.mark.smoke
    def test_get_all_products_returns_200(self, client: httpx.Client):
        response = client.get("/products")

        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert len(data["products"]) > 0

    @allure.story("Schema Validation")
    @allure.title("Product response matches Pydantic schema")
    @pytest.mark.regression
    def test_product_schema_valid(self, client: httpx.Client):
        response = client.get("/products?limit=1")

        assert response.status_code == 200
        products_response = ProductsResponse(**response.json())
        assert len(products_response.products) == 1
        product = products_response.products[0]
        assert isinstance(product, Product)

    @allure.story("Pagination")
    @allure.title("Pagination with limit={limit} and skip={skip}")
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "limit,skip",
        [
            (5, 0),
            (10, 5),
            (1, 99),
        ],
        ids=["first-5", "skip-5-take-10", "skip-99-take-1"],
    )
    def test_pagination(self, client: httpx.Client, limit: int, skip: int):
        response = client.get(f"/products?limit={limit}&skip={skip}")

        assert response.status_code == 200
        data = ProductsResponse(**response.json())
        assert data.limit == limit
        assert data.skip == skip
        assert len(data.products) <= limit

    @allure.story("Search")
    @allure.title("Search products by query string")
    @pytest.mark.regression
    def test_search_products(self, client: httpx.Client):
        response = client.get("/products/search", params={"q": "phone"})

        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        for product in data["products"]:
            assert (
                "phone" in product["title"].lower()
                or "phone" in product["description"].lower()
                or "phone" in product["category"].lower()
            )

    @allure.story("Single Product")
    @allure.title("GET /products/1 returns a valid product")
    @pytest.mark.smoke
    def test_get_single_product(self, client: httpx.Client):
        response = client.get("/products/1")

        assert response.status_code == 200
        product = Product(**response.json())
        assert product.id == 1
        assert product.title is not None

    @allure.story("Single Product")
    @allure.title("GET /products/99999 returns 404")
    @pytest.mark.negative
    def test_get_nonexistent_product_returns_404(self, client: httpx.Client):
        response = client.get("/products/99999")

        assert response.status_code == 404

    @allure.story("Categories")
    @allure.title("GET /products/categories returns a list")
    @pytest.mark.regression
    def test_get_product_categories(self, client: httpx.Client):
        response = client.get("/products/categories")

        assert response.status_code == 200
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) > 0

    @allure.story("Categories")
    @allure.title("GET products by category returns matching products")
    @pytest.mark.regression
    def test_get_products_by_category(self, client: httpx.Client):
        response = client.get("/products/category/smartphones")

        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        for product in data["products"]:
            assert product["category"] == "smartphones"

    @allure.story("CRUD")
    @allure.title("POST /products/add creates a new product")
    @pytest.mark.regression
    def test_add_product(self, client: httpx.Client):
        payload = {
            "title": "Test Product",
            "description": "A product created by automated tests",
            "price": 29.99,
            "brand": "TestBrand",
            "category": "test-category",
        }

        response = client.post("/products/add", json=payload)

        assert response.status_code in (200, 201)
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["price"] == payload["price"]
        assert "id" in data

    @allure.story("CRUD")
    @allure.title("PUT /products/1 updates an existing product")
    @pytest.mark.regression
    def test_update_product(self, client: httpx.Client):
        payload = {"title": "Updated Product Title"}

        response = client.put("/products/1", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Product Title"

    @allure.story("CRUD")
    @allure.title("DELETE /products/1 deletes a product")
    @pytest.mark.regression
    def test_delete_product(self, client: httpx.Client):
        response = client.delete("/products/1")

        assert response.status_code == 200
        data = response.json()
        assert data["isDeleted"] is True

    @allure.story("Schema Validation")
    @allure.title("Product contains all required fields")
    @pytest.mark.regression
    def test_product_has_required_fields(self, client: httpx.Client):
        response = client.get("/products/1")

        assert response.status_code == 200
        data = response.json()
        required_fields = [
            "id", "title", "description", "price",
            "discountPercentage", "rating", "stock",
            "category", "thumbnail", "images",
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    @allure.story("Data Validation")
    @allure.title("Product price is a positive number")
    @pytest.mark.regression
    def test_product_price_is_positive(self, client: httpx.Client):
        response = client.get("/products/1")

        assert response.status_code == 200
        product = Product(**response.json())
        assert product.price > 0

    @allure.story("List Products")
    @allure.title("Products total count is greater than zero")
    @pytest.mark.smoke
    def test_products_total_count(self, client: httpx.Client):
        response = client.get("/products?limit=1")

        assert response.status_code == 200
        data = ProductsResponse(**response.json())
        assert data.total > 0
