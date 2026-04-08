import allure
import httpx
import pytest

from models.cart import Cart


@allure.epic("E-Commerce API")
@allure.feature("Cart")
class TestCart:
    """Tests for the /carts endpoints."""

    @allure.story("Get Cart")
    @allure.title("GET /carts/user/1 returns the user cart")
    @pytest.mark.smoke
    def test_get_user_cart(self, client: httpx.Client):
        response = client.get("/carts/user/1")

        assert response.status_code == 200
        data = response.json()
        assert "carts" in data
        assert isinstance(data["carts"], list)

    @allure.story("CRUD")
    @allure.title("POST /carts/add creates a new cart")
    @pytest.mark.regression
    def test_add_to_cart(self, client: httpx.Client):
        payload = {
            "userId": 1,
            "products": [
                {"id": 1, "quantity": 2},
                {"id": 50, "quantity": 1},
            ],
        }

        response = client.post("/carts/add", json=payload)

        assert response.status_code in (200, 201)
        data = response.json()
        assert data["userId"] == 1
        assert len(data["products"]) == 2
        assert data["totalProducts"] == 2

    @allure.story("CRUD")
    @allure.title("PUT /carts/1 updates an existing cart")
    @pytest.mark.regression
    def test_update_cart(self, client: httpx.Client):
        payload = {
            "products": [
                {"id": 1, "quantity": 5},
            ],
        }

        response = client.put("/carts/1", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert len(data["products"]) >= 1

    @allure.story("CRUD")
    @allure.title("DELETE /carts/1 deletes a cart")
    @pytest.mark.regression
    def test_delete_cart(self, client: httpx.Client):
        response = client.delete("/carts/1")

        assert response.status_code == 200
        data = response.json()
        assert data["isDeleted"] is True

    @allure.story("Schema Validation")
    @allure.title("Cart response matches Pydantic schema")
    @pytest.mark.regression
    def test_cart_schema_valid(self, client: httpx.Client):
        response = client.get("/carts/1")

        assert response.status_code == 200
        cart = Cart(**response.json())
        assert cart.id == 1
        assert isinstance(cart.products, list)
        assert cart.totalProducts >= 0
        assert cart.totalQuantity >= 0

    @allure.story("Get Cart")
    @allure.title("GET /carts/99999 returns 404 for nonexistent cart")
    @pytest.mark.negative
    def test_get_nonexistent_cart(self, client: httpx.Client):
        response = client.get("/carts/99999")

        assert response.status_code == 404
